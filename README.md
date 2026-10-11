# Convocarte · datos

Archivo público de convocatorias culturales que usa la app **Convocarte**. La app lo descarga al abrirse y una vez por día desde:

https://raw.githubusercontent.com/fdecandia86/convocarte-datos/main/convocatorias.json

## Cómo sumar o corregir una convocatoria

1. Abrí `convocatorias.json` y tocá el lápiz (editar). Desde el celular también funciona.
2. Copiá una convocatoria parecida, pegala dentro de la lista `convocatorias` y cambiá los datos. El `id` tiene que ser único, en minúsculas y con guiones (`festival-ejemplo-2027`).
3. Cambiá `actualizado`, arriba de todo, por la fecha de hoy (`AAAA-MM-DD`).
4. Guardá con **Commit changes**. Los teléfonos lo levantan en la próxima sincronización.

Cuidá las comas y las comillas: si el JSON queda mal formado, la app no lo toma y sigue con los datos que tenía. Para revisarlo antes de guardar podés pegarlo en https://jsonlint.com.

## Campos

- `tipo`: CONCURSO, FESTIVAL, SUBSIDIO, RESIDENCIA, BECA, PREMIO, COPRODUCCION, MERCADO, LABORATORIO
- `disciplinas`: TEATRO, CINE, INMERSIVO, DANZA, MUSICA, ARTES_VISUALES, PERFORMANCE, CIRCO, TITERES, DRAMATURGIA, ARTES_DIGITALES, MULTIDISCIPLINA
- `continente`: AMERICA_LATINA, AMERICA_NORTE, EUROPA, ASIA, AFRICA, OCEANIA, MEDIO_ORIENTE, GLOBAL
- `paisesElegibles`: códigos de país de dos letras (`AR`, `ES`…) o `["*"]` si es para todo el mundo
- `perfiles`: ARTISTA, PRODUCTOR, GESTOR, COMPANIA, COLECTIVO, INSTITUCION, ESTUDIANTE
- `etapas`: IDEA, DESARROLLO, PRODUCCION, POSTPRODUCCION, ESTRENADO, CIRCULACION
- `apertura` y `cierre`: fechas `AAAA-MM-DD` o `null`
- `fechasEstimadas`: `true` si las fechas salen de la edición anterior y todavía no están confirmadas
- `periodicidad`: ANUAL, BIENAL, PERMANENTE, UNICA, SEMESTRAL

Las bases oficiales de cada convocatoria son la única fuente válida.
