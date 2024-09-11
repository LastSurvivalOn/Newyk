import json
from css_schema import html_start, html_end

class NewykHTMLMaker:
    def __init__(self) -> None:
        pass

    def _create_html_(self, data: list[dict[str, str|list[tuple[str, str]]]]) -> str:
        try:
            html = ""
            html += html_start

            for article in data['news']:
                title = article.get("title", "No Title")
                text = article.get("text", "")
                images = article.get("images", [])
                url = article.get("url", "#")

                article_html = f"""
                <div class="article">
                    <h2 style="text-align: center;">{title}</h2>
                    <p>{text}</p>
                """

                for image in images:
                    img_src = image[0]
                    img_caption = image[1] if len(image) > 1 else ""
                    article_html += f'<img src="{img_src}" alt="{img_caption}">'
                    if img_caption:
                        article_html += f'<p class="img-caption"><em>{img_caption}</em></p>'

                article_html += f'<p style="text-align: center;"><a href="{url}" target="_blank" class="Read-more">Read more</a></p>'
                article_html += "</div>"

                html += article_html

            html += html_end

            return html
        except Exception as e:
            raise Exception(f"Error with creating html text: {str(e)}")

    def _write_html_(self, html: str, file_name: str = "news_articles.html") -> None:
        try:
            with open(file_name, "w", encoding="utf-8") as output_file:
                output_file.write(html)
        except Exception as e:
            raise Exception(f"Error with writing html file: {str(e)}")
            

    def __call__(self, data: list[dict[str, str|list[tuple[str, str]]]] | str, save: bool = True, file_name: str = "news_articles.html") -> str | dict[str, str]:
        try:
            if type(data) == str:
                try:
                    with open(data, "r", encoding="utf-8") as input_file:
                        remaked_data = json.load(input_file)
                except Exception as e:
                    raise Exception(f"Error with reading json file: {str(e)}")
            elif type(data) == list:
                remaked_data = {"news": data}
            elif type(data) == dict:
                remaked_data = data
            else:
                raise Exception("Data type is not valid")
            html = self._create_html_(remaked_data)
            if save:
                self._write_html_(html, file_name)
            return html
        except Exception as e:
            return {"Error" : str(e)}
        
    

