"""
обязательно нужно реализовать 
img2words_and_styles
words_and_styles2graph
get_img2phis
"""

from pager import PageModel, PageModelUnit
from pager.page_model.sub_models import ImageModel, PDFModel, WordsAndStylesModel, SpGraph4NModel
from pager.page_model.sub_models import ImageToWordsAndCNNStyles, PDFToWordsAndCNNStyles,  WordsAndStylesToSpGraph4N
from pager.page_model.sub_models import PhisicalModel, WordsAndStylesToGLAMBlocks
from pager import PageModel, PageModelUnit, WordsAndStylesModel, SpGraph4NModel, WordsAndStylesToSpGraph4N, WordsAndStylesToSpDelaunayGraph
import os
from dotenv import load_dotenv
load_dotenv(override=True)

PATH_STYLE_MODEL = os.environ["PATH_STYLE_MODEL"]

WITH_TEXT = True
TYPE_GRAPH = "4N"
EXPERIMENT_PARAMS = {
    "node_featch": 37,
    "edge_featch": 2,
    "epochs": 50,
    "batch_size": 10,
    "learning_rate": 0.05,
    "H1": [256, 128, 64, 32, 16, 8],
    "H2": [8],
    "seg_k": 0.5
}
unit_image = PageModelUnit(id="image", 
                               sub_model=ImageModel(), 
                               converters={}, 
                               extractors=[])
    
conf_words_and_styles = {"path_model": PATH_STYLE_MODEL,"lang": "eng+rus", "psm": 4, "oem": 3,"onetone_delete": True, "k": 4 }
unit_words_and_styles = PageModelUnit(id="words_and_styles", 
                            sub_model=WordsAndStylesModel(), 
                            converters={"image": ImageToWordsAndCNNStyles(conf_words_and_styles)}, 
                            extractors=[])


unit_pdf = PageModelUnit(id="pdf", 
                               sub_model=PDFModel(), 
                               converters={}, 
                               extractors=[])

unit_words_and_styles_pdf = PageModelUnit(id="words_and_styles", 
                            sub_model=WordsAndStylesModel(), 
                            converters={"pdf": PDFToWordsAndCNNStyles()}, 
                            extractors=[])

unit_words_and_styles_start = PageModelUnit(id="words_and_styles", 
                            sub_model=WordsAndStylesModel(), 
                            converters={}, 
                            extractors=[])
conf_graph = {"with_text": True} if WITH_TEXT else None
unit_graph = PageModelUnit(id="graph", 
                            sub_model=SpGraph4NModel(), 
                            extractors=[],  
                            converters={"words_and_styles": WordsAndStylesToSpDelaunayGraph(conf_graph) 
                                                            if TYPE_GRAPH == "Delaunay" else 
                                                            WordsAndStylesToSpGraph4N(conf_graph) })
img2words_and_styles = PageModel(page_units=[
    unit_pdf, 
    unit_words_and_styles_pdf
]) # На самом деле pdf2words_and_styles

words_and_styles2graph = PageModel(page_units=[
    unit_words_and_styles_start,
    unit_graph
])


def get_img2phis(conf):
    unit_phis = PageModelUnit(id="phisical_model", 
                        sub_model=PhisicalModel(), 
                        extractors=[], 
                        converters={"words_and_styles": WordsAndStylesToGLAMBlocks(conf=conf)})
    return PageModel(page_units=[
        unit_image, 
        unit_words_and_styles,
        unit_phis
    ])


