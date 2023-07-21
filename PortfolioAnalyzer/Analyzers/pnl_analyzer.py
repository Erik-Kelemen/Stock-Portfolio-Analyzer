import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer

class PNL_Analyzer(PortfolioAnalyzer):
    def analyze(self):
        st.write("2. Profits & Losses (PnL) Analyzer")
        
        pass
    def graph(self):
        st.write("Portfolio Profits & Losses across time:")
        pass