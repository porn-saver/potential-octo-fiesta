from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
        expose_headers=["*"],  # Puedes ajustar esto según tus necesidades
        max_age=1,  # Puedes ajustar esto según tus necesidades
    )
