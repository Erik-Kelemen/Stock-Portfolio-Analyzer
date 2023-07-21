import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer

class Betas_Analyzer(PortfolioAnalyzer):
    def analyze(self):
        st.write("4. Betas Analyzer")
        
        pass
    def graph(self):
        st.write("Portfolio beta across time:")
        pass