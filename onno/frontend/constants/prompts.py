                ################################
                #                              #
                #    Knowledge Tree Prompts    #
                #                              #
                ################################

SUMMARIZATION =              '''Summarize the main ideas discussed in the text. Only include things
that are discussed in depth, not superficially mentioned. Its okay and good to say nothing and as little as possible.'''
                            
KEYWORD_SUMMARIZATION =      '''Summarize the main ideas discussed in the text. Only include things
that are discussed in depth, not superficially mentioned. Its okay and good to say nothing and as little 
as possible. If you can describe everything with very well with a few keywords, do that.'''

RANK_CATEGORIES =            '''Provided with a list of summaries of documents, which document
will best assist the user and the AI? If none of the documents are relevant, please say nothing. Rank 
the documents in order of relevance.'''  


                ################################
                #                              #
                #     Data Scraper Prompts     #
                #                              #
                ################################

CHOOSE_BEST_SCRAPED_TEXT =    '''We used multiple methods to scrape text from pdfs. Some methods 
have errors, like strange spacing characters etc. We'll provide you with the same text scraped using
different methods. Please choose the best sample out of the given numbered samples. Just say the number 
of the best one in the given JSON format.'''