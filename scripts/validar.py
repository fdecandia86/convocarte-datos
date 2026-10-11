#!/usr/bin/env python3
"""Valida convocatorias.json antes de publicarlo. Uso: python3 scripts/validar.py [archivo] [--anterior archivo_viejo]
Sale con código 1 si encuentra errores. Las advertencias no bloquean."""
import json, re, sys, datetime

ENUMS = {
    "tipo": {"CONCURSO", "FESTIVAL", "SUBSIDIO", "RESIDENCIA", "BECA", "PREMIO", "COPRODUCCION", "MERCADO", "LABORATORIO"},
    "disciplinas": {"TEATRO", "CINE", "INMERSIVO", "DANZA", "MUSICA", "ARTES_VISUALES", "PERFORMANCE", "CIRCO", "TITERES", "DRAMATURGIA", "ARTES_DIGITALES", "MULTIDISCIPLINA"},
    "continente": {"AMERICA_LATINA", "AMERICA_NORTE", "EUROPA", "ASIA", "AFRICA", "OCEANIA", "MEDIO_ORIENTE", "GLOBAL"},
    "alcance": {"NACIONAL", "REGIONAL", "INTERNACIONAL"},
    "perfiles": {"ARTISTA", "PRODUCTOR", "GESTOR", "COMPANIA", "COLECTIVO", "INSTITUCION", "ESTUDIANTE"},
    "etapas": {"IDEA", "DESARROLLO", "PRODUCCION", "POSTPRODUCCION", "ESTRENADO", "CIRCULACION"},
    "periodicidad": {"ANUAL", "BIENAL", "PERMANENTE", "UNICA", "SEMESTRAL", None},
}
PROVINCIAS_AR = {"Ciudad Autónoma de Buenos Aires", "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes",
    "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta",
    "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán"}
CAMPOS = ["id", "titulo", "organizacion", "tipo", "disciplinas", "pais", "paisNombre", "ciudad", "provincia", "provinciasElegibles",
    "continente", "lat", "lng", "alcance", "paisesElegibles", "edadMin", "edadMax", "perfiles", "etapas", "montoMax", "moneda",
    "costoInscripcion", "idiomas", "resumen", "requisitos", "documentacion", "beneficios", "apertura", "cierre", "fechasEstimadas",
    "periodicidad", "url", "urlBases", "palabrasClave", "verificado"]
LISTAS = ["disciplinas", "provinciasElegibles", "paisesElegibles", "perfiles", "etapas", "idiomas", "requisitos", "documentacion", "beneficios", "palabrasClave"]


def fecha(v):
    if v is None:
        return None
    return datetime.date.fromisoformat(v)


def validar(datos, anterior=None):
    errores, avisos = [], []
    if not isinstance(datos, dict) or not isinstance(datos.get("convocatorias"), list):
        return ["El archivo debe ser un objeto con la lista 'convocatorias'"], []
    try:
        fecha(datos.get("actualizado"))
    except Exception:
        errores.append("'actualizado' debe ser una fecha AAAA-MM-DD")
    ids = set()
    for i, c in enumerate(datos["convocatorias"]):
        nombre = f"#{i} {c.get('id', '?')}"
        faltan = [k for k in CAMPOS if k not in c]
        if faltan:
            errores.append(f"{nombre}: faltan campos {faltan}")
            continue
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", c["id"] or ""):
            errores.append(f"{nombre}: id inválido")
        if c["id"] in ids:
            errores.append(f"{nombre}: id repetido")
        ids.add(c["id"])
        if not c["titulo"] or not c["resumen"]:
            errores.append(f"{nombre}: falta título o resumen")
        for k in LISTAS:
            if not isinstance(c[k], list):
                errores.append(f"{nombre}: '{k}' debe ser una lista")
        for k, valores in ENUMS.items():
            v = c[k]
            for x in (v if isinstance(v, list) else [v]):
                if x not in valores:
                    errores.append(f"{nombre}: valor inválido en {k}: {x}")
        if not c["disciplinas"]:
            errores.append(f"{nombre}: sin disciplinas")
        if not isinstance(c["lat"], (int, float)) or not isinstance(c["lng"], (int, float)) or not (-90 <= c["lat"] <= 90 and -180 <= c["lng"] <= 180):
            errores.append(f"{nombre}: coordenadas inválidas")
        if not re.fullmatch(r"[A-Z]{2}", c["pais"] or ""):
            errores.append(f"{nombre}: país inválido")
        if c["pais"] == "AR" and c["provincia"] not in PROVINCIAS_AR:
            errores.append(f"{nombre}: provincia argentina inválida: {c['provincia']}")
        for p in c["provinciasElegibles"]:
            if c["pais"] == "AR" and p not in PROVINCIAS_AR:
                errores.append(f"{nombre}: provincia elegible inválida: {p}")
        try:
            ap, ci = fecha(c["apertura"]), fecha(c["cierre"])
            if ap and ci and ap > ci:
                errores.append(f"{nombre}: apertura posterior al cierre")
        except Exception:
            errores.append(f"{nombre}: fecha mal escrita")
        if not (c["url"] or "").startswith("http"):
            avisos.append(f"{nombre}: sin url oficial")
    if anterior:
        viejos = {c["id"] for c in anterior.get("convocatorias", [])}
        perdidos = viejos - ids
        if len(perdidos) > max(5, len(viejos) // 10):
            errores.append(f"Se borrarían {len(perdidos)} convocatorias de golpe: {sorted(perdidos)[:10]}… Revisar.")
        elif perdidos:
            avisos.append(f"Se quitan {len(perdidos)}: {sorted(perdidos)}")
    return errores, avisos


if __name__ == "__main__":
    args = sys.argv[1:]
    anterior = None
    if "--anterior" in args:
        i = args.index("--anterior")
        anterior = json.load(open(args[i + 1], encoding="utf-8"))
        del args[i:i + 2]
    ruta = args[0] if args else "convocatorias.json"
    try:
        datos = json.load(open(ruta, encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: JSON mal formado: {e}")
        sys.exit(1)
    errores, avisos = validar(datos, anterior)
    for a in avisos:
        print("aviso:", a)
    for e in errores:
        print("ERROR:", e)
    print(f"{len(datos.get('convocatorias', []))} convocatorias · {len(errores)} errores · {len(avisos)} avisos")
    sys.exit(1 if errores else 0)
