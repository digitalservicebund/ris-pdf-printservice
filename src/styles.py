import os
from weasyprint import CSS
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()

current_directory = os.path.dirname(os.path.abspath(__file__))

default_fonts = f"""
/* Normal */
@font-face {{
  font-family: "BundesSansCondWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSansCondWeb.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSansCondWeb.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}}

/* Normal */
@font-face {{
  font-family: "BundesSansWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSansWeb-Regular.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSansWeb-Regular.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}}

/* Bold */
@font-face {{
  font-family: "BundesSansWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSansWeb-Bold.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSansWeb-Bold.woff") format("woff");
  font-weight: bold;
  font-style: normal;
}}

/* Italic */
@font-face {{
  font-family: "BundesSansWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSansWeb-Italic.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSansWeb-Italic.woff") format("woff");
  font-weight: normal;
  font-style: italic;
}}

/* Bold Italic */
@font-face {{
  font-family: "BundesSansWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSansWeb-BoldItalic.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSansWeb-BoldItalic.woff") format("woff");
  font-weight: bold;
  font-style: italic;
}}

/* Normal */
@font-face {{
  font-family: "BundesSerifWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-Regular.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-Regular.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}}

/* Bold */
@font-face {{
  font-family: "BundesSerifWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-Bold.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-Bold.woff") format("woff");
  font-weight: bold;
  font-style: normal;
}}

/* Italic */
@font-face {{
  font-family: "BundesSerifWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-Italic.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-Italic.woff") format("woff");
  font-weight: normal;
  font-style: italic;
}}

/* Bold Italic */
@font-face {{
  font-family: "BundesSerifWeb";
  src: url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-BoldItalic.woff2") format("woff2"),
       url("file://{current_directory}/fonts/bundessans/BundesSerifWeb-BoldItalic.woff") format("woff");
  font-weight: bold;
  font-style: italic;
}}
"""

default_css = CSS(string=default_fonts, font_config=font_config)
