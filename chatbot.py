#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import unicodedata
from datetime import datetime

MEM_FILE = "memory.json"

def normalize(s: str) -> str:
    # remove acentos e baixa tudo
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().strip()

def load_memory() -> dict:
    if os.path.exists(MEM_FILE):
        try:
            with open(MEM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_memory(mem: dict) -> None:
    try:
        with open(MEM_FILE, "w", encoding="utf-8") as f:
            json.dump(mem, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

print("ChatBot: Oi! Eu sou o ChatBot. Como posso ajudar você hoje? (Digite 'sair' para encerrar a conversa.)")

name = None
memory = load_memory()

def remember(text: str) -> str:
    # aceita "chave: valor"
    if ":" in text:
        k, v = [t.strip() for t in text.split(":", 1)]
        if not k:
            return "Use assim: anote [chave]: [valor]."
        memory[k] = v
        save_memory(memory)
        return f"Ok, vou lembrar que {k} é {v}."
    return "Diga assim: anote [chave]: [valor]."

def delete_note(key: str) -> str:
    if key in memory:
        del memory[key]
        save_memory(memory)
        return f"Apagado: {key}."
    return f"Não encontrei a nota '{key}'."

def list_notes() -> str:
    if not memory:
        return "Você ainda não tem notas."
    linhas = [f"- {k}: {v}" for k, v in memory.items()]
    return "Suas notas:\n" + "\n".join(linhas)

def handle(msg: str) -> str:
    global name
    t = msg.strip()
    norm = normalize(t)

    # sair
    if norm in {"sair", "exit", "quit"}:
        return "EXIT"

    # nome: "me chame de X" ou "meu nome e X"
    m = re.match(r"^(me chame de|meu nome e)\s+(.+)$", norm)
    if m:
        original = t[len(m.group(1)):].strip()  # preserva maiúsculas do usuário
        name = original.title()
        return f"Prazer em conhecê-lo, {name}!"

    # horas
    if norm.startswith("que horas sao") or norm == "horas":
        return f"São {datetime.now().strftime('%H:%M')}."

    # data
    if "data de hoje" in norm or norm == "data":
        return f"Hoje é {datetime.now().strftime('%d/%m/%Y')}."

    # ecoar: "diga ..."
    m = re.match(r"^diga\s+(.+)$", norm)
    if m:
        # usa a versão original para manter acentuação
        return t[len(t.split()[0]) + 1:]

    # anotar: "anote chave: valor"
    if norm.startswith("anote "):
        return remember(t[6:].strip())

    # o que sabe sobre ...
    m = re.match(r"^o que voce sabe sobre\s+(.+)$", norm)
    if m:
        k_original = t[t.lower().find("sobre") + len("sobre"):].strip()
        return memory.get(k_original, f"Não sei nada sobre {k_original}.")

    # listar notas
    if norm in {"listar notas", "minhas notas", "listar anotações"}:
        return list_notes()

    # apagar nota: "apagar chave"
    m = re.match(r"^apagar\s+(.+)$", norm)
    if m:
        key_original = t[len(t.split()[0]) + 1:].strip()
        return delete_note(key_original)

    # ajuda
    if "ajuda" in norm or norm == "help":
        return (
            "Posso:\n"
            "- dizer horas (\"Que horas são\") e data (\"Qual a data de hoje\")\n"
            "- lembrar notas: \"Anote chave: valor\"\n"
            "- listar/apagar notas: \"Listar notas\", \"Apagar chave\"\n"
            "- ecoar: \"Diga algo aqui\"\n"
            "- guardar seu nome: \"Me chame de X\" / \"Meu nome é X\"\n"
            "- sair: \"Sair\""
        )

    # fallback
    return "Não entendi. Peça 'ajuda' para dicas."

# Loop principal
while True:
    try:
        msg = input("Você: ")
    except EOFError:
        break
    out = handle(msg)
    if out == "EXIT":
        print("ChatBot: foi bom conversar com você .Até breve!")
        break
    print("ChatBot:", out)
