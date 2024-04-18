custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'





# from shiny import App, ui, render, reactive
# import webscrape
# import summarize
# import pandas as pd
# import asyncio

# app_ui = ui.page_fluid(
#     ui.row(
#         ui.column(
#             12,
#             ui.input_text("url", "Enter URL:", value="http://example.com", width="100%"),
#             ui.input_numeric("num_articles", "Number of articles to scrape:", value=5, width="100%"),
#             ui.input_selectize("keywords", "Enter keywords:", choices=webscrape.keywords,
#                                selected=webscrape.keywords, multiple=True, width="100%"),
#             ui.input_numeric("min_length", "Minimum summary length:", value=200, width="100%"),
#             ui.input_numeric("max_length", "Maximum summary length:", value=300, width="100%"),
#             ui.input_action_button("submit", "Summarize Articles", width="100%"),
#             ui.output_table("summary", width="100%")
#         )
#     )
# )


# def server(input, output, session):
#     @output(id="summary")
#     @render.table
#     @reactive.event(input.submit)
#     async def summary():
#         progress = ui.Progress(min=0, max=100)
        
#         url = input.url()
#         num_articles = input.num_articles()
#         keywords = input.keywords()

#         articles_info = webscrape.scrape_news_site(url, custom_user_agent, max_articles=num_articles)
#         relevant_articles = webscrape.filter_articles_by_title(articles_info, keywords)

#         total = len(relevant_articles)
#         table_data = []
        
#         for i, article in enumerate(relevant_articles):
#             progress.set((i + 1) / total * 100, f"Processing article {i + 1} of {total}")
#             await asyncio.sleep(0.1)  # Simulate processing delay

#             table_data.append({
#                 'Title': article['title'],
#                 'URL': article['url'],
#                 'Summary': summarize.generate_chat_completion(article['text'], min_length=input.min_length(), max_length = input.max_length())
#             })

#         progress.close()  # Close the progress bar after processing is complete
#         return pd.DataFrame(table_data)

# app = App(app_ui, server)


from shiny import App, ui, render, reactive
import webscrape
import summarize
import pandas as pd
import asyncio

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            12,
            ui.input_text("url", "Enter URL:", value="http://example.com", width="100%"),
            ui.input_numeric("num_articles", "Number of articles to scrape:", value=5, width="100%"),
            ui.input_selectize("keywords", "Enter keywords:", choices=webscrape.keywords,
                               selected=webscrape.keywords, multiple=True, width="100%"),
            ui.input_numeric("min_length", "Minimum summary length:", value=200, width="100%"),
            ui.input_numeric("max_length", "Maximum summary length:", value=300, width="100%"),
            ui.input_action_button("submit", "Summarize Articles", width="100%"),
            ui.output_table("summary", width="100%")
        )
    )
)

def server(input, output, session):
    @output(id="summary")
    @render.table
    @reactive.event(input.submit)
    async def summary():
        
        
        url = input.url()
        num_articles = input.num_articles()
        keywords = input.keywords()

        articles_info = webscrape.scrape_news_site(url, custom_user_agent, max_articles=num_articles)
        relevant_articles = webscrape.filter_articles_by_title(articles_info, keywords)

        total = len(relevant_articles)
        table_data = []
        
        progress = ui.Progress(min=0, max=100)
        
        for i, article in enumerate(relevant_articles):
            progress.set((i + 1) / total * 100, f"Processing article {i + 1} of {total}")
            await asyncio.sleep(0.1)  # Simulate processing delay

            # Replace newline characters with spaces
            
            summary_text = summarize.generate_chat_completion(article['text'], min_length=input.min_length(), max_length=input.max_length())
            cleaned_summary = summary_text.replace('\n', ' ')

            table_data.append({
                'Title': article['title'],
                'URL': article['url'],
                'Summary': cleaned_summary
            })

        progress.close()  # Close the progress bar after processing is complete
        return pd.DataFrame(table_data)

app = App(app_ui, server)



