import sys, os
from designs import SECOES
from blocks import ENDPOINTS, FLOWS
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
def esc(s): return str(s).replace("|", "\\|")
total = {}
for slug, titulo, ds in SECOES:
    L = [f"# {titulo}", "", "> Gerado a partir das definições da base de integração. Convenções, legenda e códigos de variante: [README](README.md).", "", "## Índice", ""]
    for d in ds:
        L.append(f"- [{d['id']} — {d['titulo']}](#{d['id'].lower().replace('.', '')}) ({len(d['variantes'])} variantes)")
    n = 0
    for d in ds:
        L += ["", f"## {d['id']}", "", f"**{d['titulo']}**", "", d["resumo"], ""]
        for o in d["obs"]: L.append(f"> Observação: {o}")
        for v in d["validar"]: L.append(f"> ⚠️ A validar: {v}")
        if d["obs"] or d["validar"]: L.append("")
        for i, (nome, rows) in enumerate(d["variantes"], 1):
            n += 1
            fluxo = " → ".join(r[0] for r in rows if r[2] in ("executa", "ator", "executa (DML)") and r[6].startswith("Obrig"))
            L += [f"### {d['id']}.v{i} — {nome}", "", f"Fluxo principal: {fluxo}", "",
                  "| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade |",
                  "|---|---|---|---|---|---|---|---|"]
            for k, r in enumerate(rows, 1):
                L.append("| " + " | ".join([str(k)] + [esc(x) for x in r[:2]] + [esc(r[2]), esc(r[3]), esc(r[4]), esc(r[5]), esc(r[6])]) + " |")
            L.append("")
    total[slug] = (titulo, sum(len(d['variantes']) for d in ds), len(ds))
    open(f"{out}/{slug}.md", "w").write("\n".join(L) + "\n")
for k, v in total.items(): print(k, v)
print("TOTAL", sum(v[1] for v in total.values()))
import json
cols = ["componente", "metadata_type", "relacao", "papel", "acionado_por", "aciona", "obrigatoriedade"]
data = []
for slug, titulo, ds in SECOES:
    for d in ds:
        data.append({"secao": slug, "id": d["id"], "titulo": d["titulo"], "resumo": d["resumo"], "observacoes": d["obs"], "a_validar": d["validar"],
                     "variantes": [{"id": f"{d['id']}.v{i}", "nome": n, "componentes": [dict(ordem=k, **dict(zip(cols, r))) for k, r in enumerate(rows, 1)]}
                                   for i, (n, rows) in enumerate(d["variantes"], 1)]})
json.dump({"eixos_endpoint": ENDPOINTS, "fluxos_oauth": FLOWS, "desenhos": data}, open(f"{out}/desenhos.json", "w"), ensure_ascii=False, indent=1)
