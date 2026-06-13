from flask import Flask, request, jsonify
from sistema_notas.services.gestion_notas_service import GestionNotasService
from sistema_notas.exceptions.nota_duplicada_error import (
    NotaDuplicadaError,
    NotaFueraDeRangoError,
)
from sistema_notas.exceptions.nota_no_encontrada import (
    NotaNoEncontradaError,
)

app = Flask(__name__)
service = GestionNotasService()

@app.get("/")
def home():
    return {
        "mensaje": "Sistema de Notas funcionando"
    }

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200

@app.post("/notas")
def crear_nota():
    try:
        data = request.get_json()

        nota = service.registrar_nota(
            estudiante_id=data["estudiante_id"],
            materia_id=data["materia_id"],
            semestre=data["semestre"],
            nota=data["nota"]
        )

        return jsonify({
            "mensaje": "Nota registrada correctamente",
            "nota": {
                "estudiante_id": nota.estudiante_id,
                "materia_id": nota.materia_id,
                "semestre": nota.semestre,
                "nota": nota.nota
            }
        }), 201

    except NotaDuplicadaError as e:
        return jsonify({
            "error": str(e)
        }), 400

    except NotaFueraDeRangoError as e:
        return jsonify({
            "error": str(e)
        }), 400

@app.get("/notas")
def listar_notas():
    notas = service.listar_notas()

    return jsonify([
        {
            "estudiante_id": nota.estudiante_id,
            "materia_id": nota.materia_id,
            "semestre": nota.semestre,
            "nota": nota.nota
        }
        for nota in notas
    ])

@app.delete("/notas/<int:estudiante_id>/<materia_id>/<semestre>")
def eliminar_nota(estudiante_id, materia_id, semestre):
    try:
        service.eliminar_nota(
            estudiante_id,
            materia_id,
            semestre
        )

        return jsonify({
            "mensaje": "Nota eliminada correctamente"
        })

    except NotaNoEncontradaError as e:
        return jsonify({
            "error": str(e)
        }), 404

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )