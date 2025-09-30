#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Saúde (CLI)
-------------------------
Funcionalidades:
- IMC, % de gordura (Deurenberg), peso de gordura
- Água diária e sono recomendado
- TMB (Mifflin-St Jeor) e calorias recomendadas (por objetivo)
- Dieta sugerida e tempo/resultado esperados
- Estimativas EDUCATIVAS de Testosterona (ng/dL) e Progesterona (ng/mL)
- Entrada via terminal e exportação opcional em JSON

IMPORTANTE: Estimativas hormonais são apenas EDUCATIVAS e NÃO substituem exames
laboratoriais ou avaliação médica.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
import json

# ==============================
# Enums
# ==============================

class Sexo(Enum):
    MASCULINO = "M"
    FEMININO = "F"

class Objetivo(Enum):
    HIPERTROFIA = "hipertrofia"
    EMAGRECIMENTO = "emagrecimento"
    MANUTENCAO = "manutencao"
    DEFINICAO = "definicao"   # Novo objetivo

class FaseCiclo(Enum):
    DESCONHECIDA = "desconhecida"
    FOLICULAR = "folicular"
    OVULATORIA = "ovulatoria"
    LUTEAL = "luteal"
    MENOPAUSA = "menopausa"

# ==============================
# Classe principal
# ==============================

@dataclass
class Pessoa:
    nome: str
    peso: float               # kg
    altura: float             # metros (ex.: 1.75)
    idade: int
    sexo: Sexo
    objetivo: Objetivo
    fase_ciclo: Optional[FaseCiclo] = None  # usado para mulheres
    horas_sono: Optional[float] = None

    FATORES_ATIVIDADE: Dict[Objetivo, float] = None

    def __post_init__(self):
        # validações simples
        if self.peso <= 0:
            raise ValueError("Peso deve ser > 0.")
        if self.altura <= 0:
            raise ValueError("Altura deve ser > 0 (em metros, ex.: 1.75).")
        if self.idade <= 0:
            raise ValueError("Idade deve ser > 0.")

        if self.FATORES_ATIVIDADE is None:
            # Observação: aqui usamos um multiplicador sobre a TMB que varia com o objetivo
            # (simplificação didática; na prática, use fator de atividade física real).
            self.FATORES_ATIVIDADE = {
                Objetivo.HIPERTROFIA: 1.60,     # leve superávit
                Objetivo.EMAGRECIMENTO: 1.20,   # leve déficit
                Objetivo.MANUTENCAO: 1.40,      # manutenção
                Objetivo.DEFINICAO: 1.35,       # déficit moderado mantendo proteína alta
            }

        if self.sexo == Sexo.FEMININO:
            self.fase_ciclo = self.fase_ciclo or FaseCiclo.DESCONHECIDA

    # -------- Medidas corporais --------
    @property
    def imc(self) -> float:
        return round(self.peso / (self.altura ** 2), 2)

    @property
    def bf_percent(self) -> float:
        """Deurenberg: %BF = 1.20*IMC + 0.23*idade - 10.8*sexo(1=homem,0=mulher) - 5.4"""
        sexo_factor = 1 if self.sexo == Sexo.MASCULINO else 0
        bf = 1.20 * self.imc + 0.23 * self.idade - 10.8 * sexo_factor - 5.4
        return round(max(bf, 3.0), 2)  # limite inferior de segurança

    @property
    def peso_gordura(self) -> float:
        return round((self.bf_percent / 100.0) * self.peso, 2)

    # -------- Água e Sono --------
    @property
    def agua_diaria_litros(self) -> float:
        # regra simples ~35 mL/kg
        return round(self.peso * 0.035, 2)

    @property
    def sono_recomendado_horas(self) -> int:
        # diretriz simples por faixa etária
        if self.idade <= 18:
            return 9
        if self.idade <= 30:
            return 8
        return 7

    # -------- Energia --------
    @property
    def tmb(self) -> float:
        """Mifflin-St Jeor"""
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
            Objetivo.HIPERTROFIA: "Alto teor de proteínas, carboidratos complexos e gorduras saudáveis.",
            Objetivo.EMAGRECIMENTO: "Déficit calórico moderado, proteínas magras, vegetais e grãos integrais.",
            Objetivo.MANUTENCAO: "Alimentação equilibrada: proteínas, carboidratos e gorduras boas.",
            Objetivo.DEFINICAO: "Alta proteína, carboidrato baixo a moderado, foco em qualidade e saciedade.",
        }
        return dietas[self.objetivo]

    @property
    def tempo_estimado(self) -> str:
        if self.objetivo == Objetivo.HIPERTROFIA:
            return "6–12 meses para ganhos visíveis."
        if self.objetivo == Objetivo.EMAGRECIMENTO:
            return "3–6 meses para perda saudável de peso."
        if self.objetivo == Objetivo.DEFINICAO:
            return "8–16 semanas para reduzir gordura mantendo massa magra."
        return "Manutenção contínua com hábitos consistentes."

    @property
    def resultado_esperado(self) -> str:
        if self.objetivo == Objetivo.HIPERTROFIA:
            return "Aumento de massa muscular e força."
        if self.objetivo == Objetivo.EMAGRECIMENTO:
            return "Redução de gordura e melhora do condicionamento."
        if self.objetivo == Objetivo.DEFINICAO:
            return "Mais definição muscular com menor percentual de gordura."
        return "Peso e composição equilibrados."

    @property
    def peso_ideal(self) -> float:
        # alvos de IMC meramente ilustrativos por objetivo (educativo)
        if self.objetivo == Objetivo.HIPERTROFIA:
            imc_alvo = 24.0
        elif self.objetivo == Objetivo.EMAGRECIMENTO:
            imc_alvo = 21.0
        elif self.objetivo == Objetivo.DEFINICAO:
            imc_alvo = 22.5
        else:
            return round(self.peso, 2)
        return round(imc_alvo * (self.altura ** 2), 2)

    # -------- Hormônios (estimativas EDUCATIVAS) --------
    def estimar_testosterona(self) -> str:
        # valores-base didáticos (não clínicos)
        base = 700.0 if self.sexo == Sexo.MASCULINO else 50.0
        valor = round(base, 2)
        if self.sexo == Sexo.MASCULINO:
            faixa = "Baixa" if valor < 300 else "Normal" if valor <= 1000 else "Alta"
        else:
            faixa = "Baixa" if valor < 15 else "Normal" if valor <= 70 else "Alta"
        return f"{valor} ng/dL ({faixa})"

    def estimar_progesterona(self) -> str:
        if self.sexo == Sexo.MASCULINO:
            valor, faixa = 0.5, "Dentro do esperado"
        else:
            fase = (self.fase_ciclo or FaseCiclo.DESCONHECIDA).value
            base_por_fase = {
                "folicular": 0.5,
                "ovulatoria": 1.5,
                "luteal": 10.0,
                "menopausa": 0.4,
                "desconhecida": 1.5,
            }
            valor = round(base_por_fase.get(fase, 1.5), 2)
            faixa = "Faixa típica da fase"
        return f"{valor} ng/mL ({faixa})"

    # -------- Relatório --------
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
            "Água Recomendada (L/dia)": self.agua_diaria_litros,
            "Sono Recomendado (h)": self.sono_recomendado_horas,
            "TMB (kcal)": int(round(self.tmb)),
            "Calorias Recomendadas (kcal)": self.calorias_recomendadas,
            "Dieta Sugerida": self.dieta_sugerida,
            "Tempo Estimado": self.tempo_estimado,
            "Resultado Esperado": self.resultado_esperado,
            "Peso Ideal (kg)": self.peso_ideal,
            "Testosterona Estimada": self.estimar_testosterona(),
            "Progesterona Estimada": self.estimar_progesterona(),
            "OBS": "Estimativas hormonais são EDUCATIVAS e não substituem exames médicos.",
        }

# ==============================
# CLI
# ==============================

def coletar_dados_terminal() -> Pessoa:
    print("=== Calculadora de Saúde ===")
    nome = input("Nome: ").strip()

    def fnum(msg: str) -> float:
        return float(input(msg).replace(",", ".").strip())

    peso = fnum("Peso (kg): ")
    altura = fnum("Altura (m), ex.: 1.75: ")
    idade = int(input("Idade: ").strip())

    sexo_in = input("Sexo (M/F): ").strip().upper()
    try:
        sexo = Sexo(sexo_in)
    except ValueError:
        raise ValueError("Sexo inválido. Use 'M' ou 'F'.")

    objetivo_in = input("Objetivo (hipertrofia/emagrecimento/manutencao/definicao): ").strip().lower()
    try:
        objetivo = Objetivo(objetivo_in)
    except ValueError:
        raise ValueError("Objetivo inválido. Use: hipertrofia, emagrecimento, manutencao, definicao.")

    fase = None
    if sexo == Sexo.FEMININO:
        fase_in = input("Fase do ciclo (folicular/ovulatoria/luteal/menopausa/desconhecida): ").strip().lower()
        # valida/normaliza
        mapa_fases = {f.value: f for f in FaseCiclo}
        fase = mapa_fases.get(fase_in, FaseCiclo.DESCONHECIDA)

    return Pessoa(
        nome=nome,
        peso=peso,
        altura=altura,
        idade=idade,
        sexo=sexo,
        objetivo=objetivo,
        fase_ciclo=fase,
    )

def main():
    pessoa = coletar_dados_terminal()
    rel = pessoa.relatorio()

    print("\n=== Resultados ===")
    for k, v in rel.items():
        print(f"{k}: {v}")

    salvar = input("\nDeseja salvar em JSON? (s/n): ").strip().lower()
    if salvar == "s":
        with open("resultado.json", "w", encoding="utf-8") as f:
            json.dump(rel, f, ensure_ascii=False, indent=2)
        print("Arquivo salvo: resultado.json")

if __name__ == "__main__":
    main()
