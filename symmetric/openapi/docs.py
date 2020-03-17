"""
A module for documentation HTML methods.
"""

import flask

import symmetric.constants


def get_redoc_html(title):
    redoc_script = ("https://cdn.jsdelivr.net/npm/redoc/bundles/"
                    "redoc.standalone.js")
    google_fonts = ("https://fonts.googleapis.com/css?family=Montserrat:"
                    "300,400,700|Roboto:300,400,700")
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            <!-- needed for adaptive design -->
            <meta charset="utf-8"/>
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >
            <link href="{google_fonts}" rel="stylesheet">
            <style>
            body {{
                margin: 0;
                padding: 0;
            }}
            </style>
        </head>
            <body>
            <redoc spec-url="{symmetric.constants.OPENAPI_ROUTE}">
            </redoc>
            <script src="{redoc_script}"></script>
        </body>
    </html>
    """
    return flask.render_template_string(html)
