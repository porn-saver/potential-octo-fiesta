from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "htttp://localhost:3000"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"]  # Puedes ajustar esto según tus necesidades
    )
