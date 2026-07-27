
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Saúde Avançada (CLI + SQLite + Chatbot)
-----------------------------------------------------
Melhorias implementadas:
- Validação robusta de entradas
- Integração com SQLite (banco nativo Python) para histórico de usuários e cálculos
- Estimativas hormonais mais dinâmicas (ainda EDUCATIVAS)
- Recomendação de proteínas diárias
- Modo Chatbot interativo com compreensão de linguagem natural simples
- Menu principal com automação (salvar automático, histórico, tendências)
- Exportação para JSON/CSV
- Disclaimers claros e consistentes
- Código modular, tipado e com tratamento de erros

IMPORTANTE: 
- Estimativas hormonais, %BF (Deurenberg) e demais são EDUCATIVAS.
- NÃO substituem exames laboratoriais, avaliação médica ou nutricionista.
- Consulte sempre um profissional de saúde.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List
import json
import sqlite3
import csv
from datetime import datetime
import argparse
import sys
import re

# ==============================
# Enums (melhorados)
# ==============================

class Sexo(Enum):
    MASCULINO = "M"
    FEMININO = "F"

class Objetivo(Enum):
    HIPERTROFIA = "hipertrofia"
    EMAGRECIMENTO = "emagrecimento"
    MANUTENCAO = "manutencao"
    DEFINICAO = "definicao"

class FaseCiclo(Enum):
    DESCONHECIDA = "desconhecida"
    FOLICULAR = "folicular"
    OVULATORIA = "ovulatoria"
    LUTEAL = "luteal"
    MENOPAUSA = "menopausa"

# ==============================
# Classe de Dados (melhorada)
# ==============================

@dataclass
class Pessoa:
    nome: str
    peso: float
    altura: float
    idade: int
    sexo: Sexo
    objetivo: Objetivo
    fase_ciclo: Optional[FaseCiclo] = None
    horas_sono: Optional[float] = None
    id_usuario: Optional[int] = None  # para integração com DB

    # Constantes de classe (melhor prática)
    FATORES_ATIVIDADE: Dict[Objetivo, float] = field(default_factory=lambda: {
        Objetivo.HIPERTROFIA: 1.60,
        Objetivo.EMAGRECIMENTO: 1.20,
        Objetivo.MANUTENCAO: 1.40,
        Objetivo.DEFINICAO: 1.35,
    })

    PROTEINA_G_KG: Dict[Objetivo, float] = field(default_factory=lambda: {
        Objetivo.HIPERTROFIA: 2.0,
        Objetivo.EMAGRECIMENTO: 1.8,
        Objetivo.MANUTENCAO: 1.4,
        Objetivo.DEFINICAO: 2.2,
    })

    def __post_init__(self):
        self._validar()
        if self.sexo == Sexo.FEMININO and self.fase_ciclo is None:
            self.fase_ciclo = FaseCiclo.DESCONHECIDA

    def _validar(self):
        if not (30 <= self.peso <= 300):
            raise ValueError("Peso deve estar entre 30 e 300 kg.")
        if not (1.0 <= self.altura <= 2.5):
            raise ValueError("Altura deve estar entre 1.00 e 2.50 metros.")
        if not (5 <= self.idade <= 120):
            raise ValueError("Idade deve estar entre 5 e 120 anos.")
        if self.nome.strip() == "":
            raise ValueError("Nome não pode ser vazio.")

    # -------- Medidas corporais --------
    @property
    def imc(self) -> float:
        return round(self.peso / (self.altura ** 2), 2)

    @property
    def bf_percent(self) -> float:
        """Fórmula Deurenberg (educativa - tem limitações em atletas)"""
        sexo_factor = 1 if self.sexo == Sexo.MASCULINO else 0
        bf = 1.20 * self.imc + 0.23 * self.idade - 10.8 * sexo_factor - 5.4
        return round(max(min(bf, 60.0), 3.0), 2)

    @property
    def peso_gordura(self) -> float:
        return round((self.bf_percent / 100.0) * self.peso, 2)

    @property
    def massa_magra(self) -> float:
        return round(self.peso - self.peso_gordura, 2)

    # -------- Água, Sono e Proteínas --------
    @property
    def agua_diaria_litros(self) -> float:
        return round(self.peso * 0.035, 2)

    @property
    def sono_recomendado_horas(self) -> int:
        if self.idade <= 18:
            return 9
        if self.idade <= 30:
            return 8
        if self.idade <= 60:
            return 7
        return 7

    @property
    def proteinas_diarias_g(self) -> int:
        g_kg = self.PROTEINA_G_KG.get(self.objetivo, 1.6)
        return int(round(g_kg * self.peso))

    # -------- Energia --------
    @property
    def tmb(self) -> float:
        """Mifflin-St Jeor (padrão ouro para TMB)"""
        altura_cm = self.altura * 100.0
        s = 5 if self.sexo == Sexo.MASCULINO else -161
        return 10 * self.peso + 6.25 * altura_cm - 5 * self.idade + s

    @property
    def calorias_recomendadas(self) -> int:
        fator = self.FATORES_ATIVIDADE.get(self.objetivo, 1.4)
        return int(round(self.tmb * fator))

    # -------- Dieta / Tempo / Resultado --------
    @property
    def dieta_sugerida(self) -> str:
        dietas = {
            Objetivo.HIPERTROFIA: "Alto teor de proteínas (2.0g/kg), carboidratos complexos e gorduras saudáveis. Superávit calórico controlado.",
            Objetivo.EMAGRECIMENTO: "Déficit calórico moderado (300-500 kcal), proteínas magras altas, vegetais e fibras.",
            Objetivo.MANUTENCAO: "Alimentação equilibrada: 1.4-1.6g proteína/kg + carboidratos e gorduras de qualidade.",
            Objetivo.DEFINICAO: "Alta proteína (2.2g/kg), carboidrato baixo-moderado, foco em qualidade e saciedade.",
        }
        return dietas[self.objetivo]

    @property
    def tempo_estimado(self) -> str:
        if self.objetivo == Objetivo.HIPERTROFIA:
            return "6–12 meses para ganhos visíveis significativos (0.25-0.5kg músculo/mês)."
        if self.objetivo == Objetivo.EMAGRECIMENTO:
            return "3–6 meses para perda saudável (0.5-1kg/semana)."
        if self.objetivo == Objetivo.DEFINICAO:
            return "8–16 semanas para reduzir gordura mantendo massa magra."
        return "Manutenção contínua com hábitos consistentes."

    @property
    def resultado_esperado(self) -> str:
        if self.objetivo == Objetivo.HIPERTROFIA:
            return "Aumento de massa muscular, força e melhora da composição corporal."
        if self.objetivo == Objetivo.EMAGRECIMENTO:
            return "Redução de gordura corporal, melhora do condicionamento e saúde metabólica."
        if self.objetivo == Objetivo.DEFINICAO:
            return "Maior definição muscular com menor percentual de gordura."
        return "Peso estável e composição corporal equilibrada."

    @property
    def peso_ideal(self) -> float:
        if self.objetivo == Objetivo.HIPERTROFIA:
            imc_alvo = 24.5
        elif self.objetivo == Objetivo.EMAGRECIMENTO:
            imc_alvo = 21.5
        elif self.objetivo == Objetivo.DEFINICAO:
            imc_alvo = 22.0
        else:
            return round(self.peso, 2)
        return round(imc_alvo * (self.altura ** 2), 2)

    # -------- Hormônios (ESTIMATIVAS EDUCATIVAS - NÃO CLÍNICAS) --------
    def estimar_testosterona(self) -> str:
        """Estimativa didática baseada em idade e sexo (valores médios populacionais)"""
        if self.sexo == Sexo.MASCULINO:
            # Queda aproximada de ~1% ao ano após os 30
            base = 650 - max(0, (self.idade - 30) * 4.5)
            base = max(base, 300)
            valor = round(base, 0)
            if valor < 300:
                faixa = "Possivelmente baixa (consulte médico)"
            elif valor <= 1000:
                faixa = "Faixa normal (média populacional)"
            else:
                faixa = "Alta (raro em estimativa)"
        else:
            # Mulheres: muito mais baixa e variável
            base = 45 - max(0, (self.idade - 35) * 0.8)
            base = max(base, 10)
            valor = round(base, 0)
            if valor < 15:
                faixa = "Baixa (comum na menopausa)"
            elif valor <= 70:
                faixa = "Normal para mulheres"
            else:
                faixa = "Elevada (pode indicar SOP)"
        return f"{int(valor)} ng/dL ({faixa}) — Estimativa EDUCATIVA"

    def estimar_progesterona(self) -> str:
        if self.sexo == Sexo.MASCULINO:
            return "0.4–0.6 ng/mL (faixa normal masculina) — Estimativa EDUCATIVA"
        else:
            fase = (self.fase_ciclo or FaseCiclo.DESCONHECIDA).value
            base_por_fase = {
                "folicular": (0.3, 1.0, "Baixa (fase folicular)"),
                "ovulatoria": (1.0, 2.0, "Pico ovulatório"),
                "luteal": (8.0, 20.0, "Alta (fase lútea)"),
                "menopausa": (0.2, 0.8, "Baixa (menopausa)"),
                "desconhecida": (1.0, 5.0, "Média (fase desconhecida)"),
            }
            min_v, max_v, faixa = base_por_fase.get(fase, (1.0, 5.0, "Média"))
            valor = round((min_v + max_v) / 2, 1)
            return f"{valor} ng/mL ({faixa}) — Estimativa EDUCATIVA"

    # -------- Relatório completo --------
    def relatorio(self) -> Dict[str, Any]:
        return {
            "Nome": self.nome,
            "Sexo": self.sexo.value,
            "Idade": self.idade,
            "Altura (m)": round(self.altura, 2),
            "Peso (kg)": round(self.peso, 2),
            "IMC": self.imc,
            "Gordura Corporal (%)": self.bf_percent,
            "Peso de Gordura (kg)": self.peso_gordura,
            "Massa Magra (kg)": self.massa_magra,
            "Água Recomendada (L/dia)": self.agua_diaria_litros,
            "Sono Recomendado (h)": self.sono_recomendado_horas,
            "Proteínas Diárias (g)": self.proteinas_diarias_g,
            "TMB (kcal)": int(round(self.tmb)),
            "Calorias Recomendadas (kcal)": self.calorias_recomendadas,
            "Dieta Sugerida": self.dieta_sugerida,
            "Tempo Estimado": self.tempo_estimado,
            "Resultado Esperado": self.resultado_esperado,
            "Peso Ideal (kg)": self.peso_ideal,
            "Testosterona Estimada": self.estimar_testosterona(),
            "Progesterona Estimada": self.estimar_progesterona(),
            "Data do Cálculo": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "OBS": "Estimativas hormonais e %BF são EDUCATIVAS e não substituem exames médicos ou avaliação profissional.",
        }

# ==============================
# Gerenciador de Banco de Dados (SQLite nativo)
# ==============================

class DatabaseManager:
    def __init__(self, db_path: str = "saude_calculadora.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._criar_tabelas()

    def _criar_tabelas(self):
        cursor = self.conn.cursor()
        # Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sexo TEXT NOT NULL,
                idade INTEGER NOT NULL,
                altura REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Histórico de cálculos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                peso REAL NOT NULL,
                imc REAL,
                bf_percent REAL,
                tmb INTEGER,
                calorias INTEGER,
                objetivo TEXT,
                resultado_json TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        self.conn.commit()

    def salvar_ou_atualizar_usuario(self, pessoa: Pessoa) -> int:
        cursor = self.conn.cursor()
        if pessoa.id_usuario:
            cursor.execute("""
                UPDATE usuarios SET nome=?, sexo=?, idade=?, altura=? WHERE id=?
            """, (pessoa.nome, pessoa.sexo.value, pessoa.idade, pessoa.altura, pessoa.id_usuario))
            user_id = pessoa.id_usuario
        else:
            cursor.execute("""
                INSERT INTO usuarios (nome, sexo, idade, altura)
                VALUES (?, ?, ?, ?)
            """, (pessoa.nome, pessoa.sexo.value, pessoa.idade, pessoa.altura))
            user_id = cursor.lastrowid
        self.conn.commit()
        return user_id

    def salvar_calculo(self, usuario_id: int, rel: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO calculos (usuario_id, peso, imc, bf_percent, tmb, calorias, objetivo, resultado_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario_id,
            rel["Peso (kg)"],
            rel["IMC"],
            rel["Gordura Corporal (%)"],
            rel["TMB (kcal)"],
            rel["Calorias Recomendadas (kcal)"],
            rel.get("Objetivo", "N/A"),
            json.dumps(rel, ensure_ascii=False)
        ))
        self.conn.commit()

    def listar_usuarios(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def carregar_usuario(self, user_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def obter_historico(self, usuario_id: int, limite: int = 10) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, peso, imc, bf_percent, calorias, objetivo
            FROM calculos 
            WHERE usuario_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (usuario_id, limite))
        return [dict(row) for row in cursor.fetchall()]

    def exportar_historico_csv(self, usuario_id: int, arquivo: str = "historico.csv"):
        historico = self.obter_historico(usuario_id, limite=1000)
        if not historico:
            return False
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=historico[0].keys())
            writer.writeheader()
            writer.writerows(historico)
        return True

    def fechar(self):
        self.conn.close()

# ==============================
# Chatbot Inteligente (baseado em regras + estado)
# ==============================

class ChatbotSaude:
    def __init__(self, db: DatabaseManager, pessoa_atual: Optional[Pessoa] = None):
        self.db = db
        self.pessoa = pessoa_atual
        self.historico_chat = []

    def definir_pessoa(self, pessoa: Pessoa):
        self.pessoa = pessoa

    def responder(self, mensagem: str) -> str:
        msg = mensagem.lower().strip()
        self.historico_chat.append(("user", mensagem))

        if not self.pessoa:
            return ("Olá! Para eu te ajudar com cálculos personalizados, primeiro faça uma avaliação "
                    "ou carregue um usuário existente. Digite 'menu' para voltar.")

        # Comandos diretos
        if any(x in msg for x in ["imc", "índice de massa"]):
            return f"Seu IMC atual é **{self.pessoa.imc}** (classificação: {self._classificar_imc()})."

        if any(x in msg for x in ["gordura", "%bf", "percentual de gordura"]):
            return f"Seu percentual de gordura corporal estimado é **{self.pessoa.bf_percent}%**."

        if any(x in msg for x in ["caloria", "kcal", "energia"]):
            return (f"TMB: **{int(self.pessoa.tmb)} kcal**\n"
                    f"Calorias recomendadas para {self.pessoa.objetivo.value}: **{self.pessoa.calorias_recomendadas} kcal**")

        if any(x in msg for x in ["proteína", "proteina", "g de proteína"]):
            return f"Recomendação diária de proteínas: **{self.pessoa.proteinas_diarias_g}g** ({self.pessoa.PROTEINA_G_KG[self.pessoa.objetivo]}g/kg)."

        if any(x in msg for x in ["água", "agua", "hidratação"]):
            return f"Água recomendada: **{self.pessoa.agua_diaria_litros} litros/dia**."

        if any(x in msg for x in ["sono", "dormir"]):
            return f"Sono recomendado: **{self.pessoa.sono_recomendado_horas} horas/noite**."

        if any(x in msg for x in ["dieta", "alimentação", "comer"]):
            return f"**Dieta sugerida:** {self.pessoa.dieta_sugerida}\n\n**Tempo estimado:** {self.pessoa.tempo_estimado}"

        if any(x in msg for x in ["testosterona", "testo"]):
            return self.pessoa.estimar_testosterona()

        if any(x in msg for x in ["progesterona", "progest"]):
            return self.pessoa.estimar_progesterona()

        if any(x in msg for x in ["histórico", "historico", "progresso", "evolução"]):
            return self._mostrar_historico_resumido()

        if any(x in msg for x in ["peso ideal", "peso alvo"]):
            return f"Peso ideal estimado para seu objetivo: **{self.pessoa.peso_ideal} kg**"

        if any(x in msg for x in ["resultado", "expectativa"]):
            return self.pessoa.resultado_esperado

        if "menu" in msg or "voltar" in msg:
            return "Voltando ao menu principal..."

        # Resposta genérica inteligente
        return ("Não entendi completamente. Tente perguntas como:\n"
                "• Qual meu IMC?\n"
                "• Quanto de proteína devo comer?\n"
                "• Me mostre meu histórico\n"
                "• Sugira uma dieta\n"
                "• Qual minha testosterona estimada?\n\n"
                "Ou digite 'sair' para encerrar o chatbot.")

    def _classificar_imc(self) -> str:
        imc = self.pessoa.imc
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"

    def _mostrar_historico_resumido(self) -> str:
        if not self.pessoa.id_usuario:
            return "Nenhum histórico salvo ainda (faça uma avaliação primeiro)."
        hist = self.db.obter_historico(self.pessoa.id_usuario, limite=5)
        if not hist:
            return "Ainda não há cálculos anteriores salvos."
        linhas = ["Últimas medições:"]
        for h in hist:
            linhas.append(f"• {h['timestamp'][:10]} | Peso: {h['peso']}kg | IMC: {h['imc']} | Gordura: {h['bf_percent']}%")
        return "\n".join(linhas)

# ==============================
# Interface CLI Principal
# ==============================

def coletar_dados_terminal(db: Optional[DatabaseManager] = None) -> Pessoa:
    print("\n=== Nova Avaliação de Saúde ===")
    nome = input("Nome: ").strip()

    def fnum(msg: str, minimo: float, maximo: float) -> float:
        while True:
            try:
                val = float(input(msg).replace(",", ".").strip())
                if minimo <= val <= maximo:
                    return val
                print(f"Valor deve estar entre {minimo} e {maximo}.")
            except ValueError:
                print("Entrada inválida. Use números (ex: 1.75 ou 75,5).")

    peso = fnum("Peso (kg): ", 30, 300)
    altura = fnum("Altura (m, ex: 1.75): ", 1.0, 2.5)
    idade = int(fnum("Idade: ", 5, 120))

    while True:
        sexo_in = input("Sexo (M/F): ").strip().upper()
        if sexo_in in ["M", "F"]:
            sexo = Sexo(sexo_in)
            break
        print("Use 'M' ou 'F'.")

    objetivos_validos = [o.value for o in Objetivo]
    while True:
        objetivo_in = input(f"Objetivo ({'/'.join(objetivos_validos)}): ").strip().lower()
        if objetivo_in in objetivos_validos:
            objetivo = Objetivo(objetivo_in)
            break
        print("Objetivo inválido.")

    fase = None
    if sexo == Sexo.FEMININO:
        fases_validas = [f.value for f in FaseCiclo]
        while True:
            fase_in = input(f"Fase do ciclo ({'/'.join(fases_validas)}): ").strip().lower()
            if fase_in in fases_validas:
                fase = FaseCiclo(fase_in)
                break
            print("Fase inválida.")

    pessoa = Pessoa(
        nome=nome,
        peso=peso,
        altura=altura,
        idade=idade,
        sexo=sexo,
        objetivo=objetivo,
        fase_ciclo=fase,
    )

    # Salvar automaticamente no banco
    if db:
        user_id = db.salvar_ou_atualizar_usuario(pessoa)
        pessoa.id_usuario = user_id
        rel = pessoa.relatorio()
        db.salvar_calculo(user_id, rel)
        print(f"\n✅ Dados salvos automaticamente no banco (ID usuário: {user_id})")

    return pessoa

def mostrar_relatorio(pessoa: Pessoa):
    rel = pessoa.relatorio()
    print("\n" + "="*60)
    print("           RELATÓRIO DE SAÚDE PERSONALIZADO")
    print("="*60)
    for k, v in rel.items():
        if k != "OBS":
            print(f"{k:30}: {v}")
    print("-"*60)
    print(rel["OBS"])
    print("="*60)

def menu_principal():
    parser = argparse.ArgumentParser(description="Calculadora de Saúde Avançada")
    parser.add_argument("--chat", action="store_true", help="Iniciar diretamente no modo chatbot")
    args = parser.parse_args()

    db = DatabaseManager()
    chatbot = ChatbotSaude(db)
    pessoa_atual: Optional[Pessoa] = None

    if args.chat:
        print("=== Modo Chatbot Ativado ===")
        print("Digite suas perguntas ou 'sair' para voltar ao menu.")
        while True:
            try:
                msg = input("\nVocê: ").strip()
                if msg.lower() in ["sair", "exit", "quit", "menu"]:
                    break
                resposta = chatbot.responder(msg)
                print(f"\nBot: {resposta}")
            except KeyboardInterrupt:
                break
        return

    while True:
        print("\n" + "="*50)
        print("      CALCULADORA DE SAÚDE AVANÇADA v2.0")
        print("="*50)
        print("1. Nova avaliação + salvar no banco")
        print("2. Carregar usuário existente")
        print("3. Ver meu histórico e tendências")
        print("4. Iniciar Chatbot (perguntas em linguagem natural)")
        print("5. Exportar histórico para CSV")
        print("6. Sair")
        print("-"*50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                pessoa_atual = coletar_dados_terminal(db)
                mostrar_relatorio(pessoa_atual)
                chatbot.definir_pessoa(pessoa_atual)
            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "2":
            usuarios = db.listar_usuarios()
            if not usuarios:
                print("Nenhum usuário cadastrado ainda.")
                continue
            print("\nUsuários cadastrados:")
            for u in usuarios:
                print(f"  [{u['id']}] {u['nome']} ({u['sexo']}, {u['idade']} anos)")
            try:
                uid = int(input("\nDigite o ID do usuário: "))
                user_data = db.carregar_usuario(uid)
                if user_data:
                    # Recriar Pessoa com dados básicos (peso atual será perguntado)
                    print(f"\nUsuário carregado: {user_data['nome']}")
                    novo_peso = float(input("Peso atual (kg): ").replace(",", "."))
                    pessoa_atual = Pessoa(
                        nome=user_data['nome'],
                        peso=novo_peso,
                        altura=user_data['altura'],
                        idade=user_data['idade'],
                        sexo=Sexo(user_data['sexo']),
                        objetivo=Objetivo.MANUTENCAO,  # default
                        id_usuario=uid
                    )
                    # Perguntar objetivo atual
                    obj_in = input("Objetivo atual (hipertrofia/emagrecimento/manutencao/definicao): ").lower()
                    if obj_in in [o.value for o in Objetivo]:
                        pessoa_atual.objetivo = Objetivo(obj_in)
                    rel = pessoa_atual.relatorio()
                    db.salvar_calculo(uid, rel)
                    mostrar_relatorio(pessoa_atual)
                    chatbot.definir_pessoa(pessoa_atual)
            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "3":
            if not pessoa_atual or not pessoa_atual.id_usuario:
                print("Faça uma avaliação primeiro ou carregue um usuário.")
                continue
            hist = db.obter_historico(pessoa_atual.id_usuario, limite=8)
            if not hist:
                print("Sem histórico ainda.")
                continue
            print("\n=== Seu Histórico Recente ===")
            print(f"{'Data':<12} {'Peso':>8} {'IMC':>6} {'%Gordura':>10} {'Calorias':>10}")
            print("-"*50)
            for h in hist:
                print(f"{h['timestamp'][:10]:<12} {h['peso']:>8.1f} {h['imc']:>6.1f} {h['bf_percent']:>9.1f}% {h['calorias']:>10}")
            print("\nDica: Use o chatbot e pergunte 'meu histórico' para resumo.")

        elif opcao == "4":
            if not pessoa_atual:
                print("Faça uma avaliação primeiro para ativar o chatbot personalizado.")
                continue
            chatbot.definir_pessoa(pessoa_atual)
            print("\n=== Chatbot de Saúde ===")
            print("Exemplos: 'qual meu imc?', 'quanto de proteína?', 'meu histórico', 'sair'")
            while True:
                try:
                    msg = input("\nVocê: ").strip()
                    if msg.lower() in ["sair", "exit", "quit", "voltar"]:
                        break
                    resposta = chatbot.responder(msg)
                    print(f"Bot: {resposta}")
                except KeyboardInterrupt:
                    break

        elif opcao == "5":
            if not pessoa_atual or not pessoa_atual.id_usuario:
                print("Carregue ou crie um usuário primeiro.")
                continue
            arquivo = input("Nome do arquivo CSV (padrão: historico.csv): ").strip() or "historico.csv"
            if db.exportar_historico_csv(pessoa_atual.id_usuario, arquivo):
                print(f"✅ Histórico exportado para {arquivo}")
            else:
                print("Nenhum dado para exportar.")

        elif opcao == "6":
            print("\nObrigado por usar a Calculadora de Saúde Avançada!")
            print("Lembrete: Mantenha hábitos saudáveis e consulte profissionais.")
            db.fechar()
            sys.exit(0)

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal() #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Saúde Mental (CLI + SQLite)
-----------------------------------------
Objetivo:
- Avaliar sinais emocionais e de bem-estar de forma simples e educativa.
- Armazenar avaliações em banco SQLite nativo do Python.
- Ajudar a acompanhar padrões ao longo do tempo.

Importante:
- Esta ferramenta não substitui avaliação psicológica ou psiquiátrica.
- Se houver sofrimento intenso, pensamentos de autolesão ou risco, procure ajuda profissional imediatamente.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import csv
import json
import sqlite3
import sys
from datetime import datetime


@dataclass
class AvaliacaoMental:
    nome: str
    idade: int
    humor: int
    ansiedade: int
    estresse: int
    sono: int
    conexoes: int
    energia: int
    id_usuario: Optional[int] = None

    def __post_init__(self):
        self._validar()

    def _validar(self):
        if not self.nome.strip():
            raise ValueError("Nome não pode estar vazio.")
        if not (5 <= self.idade <= 120):
            raise ValueError("Idade deve estar entre 5 e 120 anos.")
        for campo in ["humor", "ansiedade", "estresse", "sono", "conexoes", "energia"]:
            valor = getattr(self, campo)
            if not (1 <= valor <= 10):
                raise ValueError(f"{campo} deve estar entre 1 e 10.")

    @property
    def score(self) -> int:
        total = (
            self.humor
            + (11 - self.ansiedade)
            + (11 - self.estresse)
            + self.sono
            + self.conexoes
            + self.energia
        )
        return int(round(total / 6))

    @property
    def classificacao(self) -> str:
        if self.score >= 8:
            return "Bom equilíbrio emocional"
        if self.score >= 6:
            return "Em observação"
        if self.score >= 4:
            return "Requer atenção"
        return "Sugere apoio profissional"

    def relatorio(self) -> Dict[str, Any]:
        return {
            "Nome": self.nome,
            "Idade": self.idade,
            "Humor": self.humor,
            "Ansiedade": self.ansiedade,
            "Estresse": self.estresse,
            "Sono": self.sono,
            "Conexões sociais": self.conexoes,
            "Energia": self.energia,
            "Score emocional": self.score,
            "Classificação": self.classificacao,
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "OBS": "Esta avaliação é educativa e não substitui diagnóstico profissional.",
        }


class DatabaseManager:
    def __init__(self, db_path: str = "saude_mental.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._criar_tabelas()

    def _criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                humor INTEGER NOT NULL,
                ansiedade INTEGER NOT NULL,
                estresse INTEGER NOT NULL,
                sono INTEGER NOT NULL,
                conexoes INTEGER NOT NULL,
                energia INTEGER NOT NULL,
                score INTEGER NOT NULL,
                classificacao TEXT NOT NULL,
                resultado_json TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
            """
        )
        self.conn.commit()

    def salvar_ou_atualizar_usuario(self, avaliacao: AvaliacaoMental) -> int:
        cursor = self.conn.cursor()
        if avaliacao.id_usuario:
            cursor.execute(
                "UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?",
                (avaliacao.nome, avaliacao.idade, avaliacao.id_usuario),
            )
            user_id = avaliacao.id_usuario
        else:
            cursor.execute(
                "INSERT INTO usuarios (nome, idade) VALUES (?, ?)",
                (avaliacao.nome, avaliacao.idade),
            )
            user_id = cursor.lastrowid
        self.conn.commit()
        return user_id

    def salvar_avaliacao(self, usuario_id: int, rel: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO avaliacoes (
                usuario_id, humor, ansiedade, estresse, sono, conexoes, energia, score, classificacao, resultado_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                usuario_id,
                rel["Humor"],
                rel["Ansiedade"],
                rel["Estresse"],
                rel["Sono"],
                rel["Conexões sociais"],
                rel["Energia"],
                rel["Score emocional"],
                rel["Classificação"],
                json.dumps(rel, ensure_ascii=False),
            ),
        )
        self.conn.commit()

    def listar_usuarios(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def carregar_usuario(self, user_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def obter_historico(self, usuario_id: int, limite: int = 10) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT timestamp, score, classificacao, humor, ansiedade, estresse, sono, conexoes, energia
            FROM avaliacoes
            WHERE usuario_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (usuario_id, limite),
        )
        return [dict(row) for row in cursor.fetchall()]

    def exportar_historico_json(self, usuario_id: int, arquivo: str = "historico_mental.json") -> bool:
        historico = self.obter_historico(usuario_id, limite=1000)
        if not historico:
            return False
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        return True

    def exportar_historico_csv(self, usuario_id: int, arquivo: str = "historico_mental.csv") -> bool:
        historico = self.obter_historico(usuario_id, limite=1000)
        if not historico:
            return False
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=historico[0].keys())
            writer.writeheader()
            writer.writerows(historico)
        return True

    def fechar(self):
        self.conn.close()


def coletar_dados_terminal(db: Optional[DatabaseManager] = None) -> AvaliacaoMental:
    print("\n=== Nova Avaliação de Saúde Mental ===")
    nome = input("Nome: ").strip()

    def pedir_int(msg: str, minimo: int, maximo: int) -> int:
        while True:
            try:
                valor = int(input(msg).strip())
                if minimo <= valor <= maximo:
                    return valor
                print(f"Valor deve estar entre {minimo} e {maximo}.")
            except ValueError:
                print("Entrada inválida. Use um número inteiro.")

    idade = pedir_int("Idade: ", 5, 120)
    humor = pedir_int("Humor (1 a 10): ", 1, 10)
    ansiedade = pedir_int("Ansiedade (1 a 10, 1 = pouca, 10 = muita): ", 1, 10)
    estresse = pedir_int("Estresse (1 a 10): ", 1, 10)
    sono = pedir_int("Qualidade do sono (1 a 10): ", 1, 10)
    conexoes = pedir_int("Conexões sociais (1 a 10): ", 1, 10)
    energia = pedir_int("Energia (1 a 10): ", 1, 10)

    avaliacao = AvaliacaoMental(
        nome=nome,
        idade=idade,
        humor=humor,
        ansiedade=ansiedade,
        estresse=estresse,
        sono=sono,
        conexoes=conexoes,
        energia=energia,
    )

    if db:
        user_id = db.salvar_ou_atualizar_usuario(avaliacao)
        avaliacao.id_usuario = user_id
        rel = avaliacao.relatorio()
        db.salvar_avaliacao(user_id, rel)
        print(f"\n✅ Avaliação salva automaticamente no banco (ID usuário: {user_id})")

    return avaliacao


def mostrar_relatorio(avaliacao: AvaliacaoMental):
    rel = avaliacao.relatorio()
    print("\n" + "=" * 60)
    print("         RELATÓRIO DE SAÚDE MENTAL")
    print("=" * 60)
    for chave, valor in rel.items():
        if chave != "OBS":
            print(f"{chave:<24}: {valor}")
    print("-" * 60)
    print(rel["OBS"])
    print("=" * 60)


def menu_principal():
    db = DatabaseManager()
    usuario_atual: Optional[AvaliacaoMental] = None

    while True:
        print("\n" + "=" * 50)
        print("      AVALIADOR DE SAÚDE MENTAL")
        print("=" * 50)
        print("1. Nova avaliação")
        print("2. Carregar usuário existente")
        print("3. Ver histórico")
        print("4. Exportar histórico para JSON")
        print("5. Exportar histórico para CSV")
        print("6. Sair")
        print("-" * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                usuario_atual = coletar_dados_terminal(db)
                mostrar_relatorio(usuario_atual)
            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "2":
            usuarios = db.listar_usuarios()
            if not usuarios:
                print("Nenhum usuário cadastrado ainda.")
                continue
            print("\nUsuários cadastrados:")
            for u in usuarios:
                print(f"  [{u['id']}] {u['nome']} ({u['idade']} anos)")
            try:
                user_id = int(input("\nDigite o ID do usuário: ").strip())
                user_data = db.carregar_usuario(user_id)
                if user_data:
                    print(f"\nUsuário carregado: {user_data['nome']}")
                    usuario_atual = AvaliacaoMental(
                        nome=user_data["nome"],
                        idade=user_data["idade"],
                        humor=5,
                        ansiedade=5,
                        estresse=5,
                        sono=5,
                        conexoes=5,
                        energia=5,
                        id_usuario=user_id,
                    )
                    rel = usuario_atual.relatorio()
                    db.salvar_avaliacao(user_id, rel)
                    mostrar_relatorio(usuario_atual)
            except Exception as e:
                print(f"Erro: {e}")

        elif opcao == "3":
            if not usuario_atual or not usuario_atual.id_usuario:
                print("Faça uma avaliação primeiro ou carregue um usuário.")
                continue
            historico = db.obter_historico(usuario_atual.id_usuario, limite=8)
            if not historico:
                print("Sem histórico ainda.")
                continue
            print("\n=== Seu histórico recente ===")
            print(f"{'Data':<12} {'Score':>6} {'Classificação':<20}")
            print("-" * 45)
            for item in historico:
                print(f"{item['timestamp'][:10]:<12} {item['score']:>6} {item['classificacao']:<20}")

        elif opcao == "4":
            if not usuario_atual or not usuario_atual.id_usuario:
                print("Carregue ou crie um usuário primeiro.")
                continue
            arquivo = input("Nome do arquivo JSON (padrão: historico_mental.json): ").strip() or "historico_mental.json"
            if db.exportar_historico_json(usuario_atual.id_usuario, arquivo):
                print(f"✅ Histórico exportado para {arquivo}")
            else:
                print("Nenhum dado para exportar.")

        elif opcao == "5":
            if not usuario_atual or not usuario_atual.id_usuario:
                print("Carregue ou crie um usuário primeiro.")
                continue
            arquivo = input("Nome do arquivo CSV (padrão: historico_mental.csv): ").strip() or "historico_mental.csv"
            if db.exportar_historico_csv(usuario_atual.id_usuario, arquivo):
                print(f"✅ Histórico exportado para {arquivo}")
            else:
                print("Nenhum dado para exportar.")

        elif opcao == "6":
            print("\nObrigado por usar a calculadora de saúde mental!")
            print("Lembre-se: cuidado emocional e apoio profissional fazem parte do processo.")
            db.fechar()
            sys.exit(0)

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()