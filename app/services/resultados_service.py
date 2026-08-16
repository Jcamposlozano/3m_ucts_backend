from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.evaluacion import Evaluacion
from app.models.jurado import Jurado
from app.models.participante import Participante
from app.models.voto_publico import VotoPublico


def obtener_resultados_admin(
    db: Session
):

    # =========================================================
    # PARTICIPANTES ACTIVOS
    # =========================================================

    participantes = list(
        db.scalars(
            select(Participante)
            .where(
                Participante.activo.is_(True)
            )
            .order_by(
                Participante.codigo
            )
        ).all()
    )


    # =========================================================
    # JURADOS ACTIVOS
    # =========================================================

    jurados = list(
        db.scalars(
            select(Jurado)
            .where(
                Jurado.activo.is_(True)
            )
            .order_by(
                Jurado.id
            )
        ).all()
    )


    # =========================================================
    # EVALUACIONES FINALIZADAS
    # =========================================================

    evaluaciones = list(
        db.scalars(
            select(Evaluacion)
            .where(
                Evaluacion.estado == "FINALIZADA"
            )
        ).all()
    )


    # =========================================================
    # CONTEO DE VOTOS PÚBLICOS POR PARTICIPANTE
    # =========================================================

    votos_query = (
        select(
            VotoPublico.participante_id,
            func.count(
                VotoPublico.id
            ).label(
                "total_votos"
            )
        )
        .group_by(
            VotoPublico.participante_id
        )
    )


    votos_resultado = db.execute(
        votos_query
    ).all()


    votos_por_participante = {
        fila.participante_id:
            fila.total_votos

        for fila in votos_resultado
    }


    # =========================================================
    # DICCIONARIO DE JURADOS
    # =========================================================

    jurados_por_id = {
        jurado.id:
            jurado

        for jurado in jurados
    }


    # =========================================================
    # AGRUPAR EVALUACIONES POR PARTICIPANTE
    # =========================================================

    evaluaciones_por_participante = {}


    for evaluacion in evaluaciones:

        if (
            evaluacion.participante_id
            not in evaluaciones_por_participante
        ):

            evaluaciones_por_participante[
                evaluacion.participante_id
            ] = []


        evaluaciones_por_participante[
            evaluacion.participante_id
        ].append(
            evaluacion
        )


    # =========================================================
    # CONSTRUIR RESULTADOS
    # =========================================================

    resultados = []


    for participante in participantes:

        evaluaciones_participante = (
            evaluaciones_por_participante.get(
                participante.id,
                []
            )
        )


        detalle_jurados = []

        puntajes = []


        for evaluacion in evaluaciones_participante:

            jurado = jurados_por_id.get(
                evaluacion.jurado_id
            )


            if not jurado:
                continue


            if evaluacion.puntaje_total is None:
                continue


            puntaje = float(
                evaluacion.puntaje_total
            )


            puntajes.append(
                puntaje
            )


            detalle_jurados.append(
                {
                    "jurado_id":
                        jurado.id,

                    "nombre":
                        jurado.nombre,

                    "puntaje":
                        puntaje,

                    "evaluacion_id":
                        evaluacion.id
                }
            )


        # =====================================================
        # PROMEDIO
        # =====================================================

        promedio = None


        if puntajes:

            promedio = round(
                sum(puntajes)
                / len(puntajes),
                2
            )


        # =====================================================
        # REGISTRO PARTICIPANTE
        # =====================================================

        resultados.append(
            {
                "ranking":
                    None,

                "participante_id":
                    participante.id,

                "codigo":
                    participante.codigo,

                "nombre":
                    participante.nombre,

                "programa_doctoral":
                    participante.programa_doctoral,

                "titulo_presentacion":
                    participante.titulo_presentacion,

                "cantidad_evaluaciones":
                    len(puntajes),

                "promedio":
                    promedio,

                "jurados":
                    detalle_jurados,

                "votos_publicos":
                    votos_por_participante.get(
                        participante.id,
                        0
                    )
            }
        )


    # =========================================================
    # ORDENAR POR PROMEDIO
    # =========================================================

    resultados.sort(
        key=lambda item: (
            item["promedio"] is not None,
            item["promedio"]
            if item["promedio"] is not None
            else -1
        ),
        reverse=True
    )


    # =========================================================
    # ASIGNAR RANKING
    # =========================================================

    posicion = 1


    for resultado in resultados:

        if resultado["promedio"] is None:

            resultado["ranking"] = None

        else:

            resultado["ranking"] = posicion

            posicion += 1


    # =========================================================
    # TOTAL VOTOS
    # =========================================================

    total_votos_publicos = sum(
        votos_por_participante.values()
    )


    # =========================================================
    # RESPUESTA FINAL
    # =========================================================

    return {
        "total_participantes":
            len(participantes),

        "total_evaluaciones_finalizadas":
            len(evaluaciones),

        "total_votos_publicos":
            total_votos_publicos,

        "jurados": [
            {
                "id":
                    jurado.id,

                "nombre":
                    jurado.nombre
            }

            for jurado in jurados
        ],

        "resultados":
            resultados
    }