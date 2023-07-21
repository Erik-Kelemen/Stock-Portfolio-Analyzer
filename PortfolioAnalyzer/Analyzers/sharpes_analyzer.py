import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..portfolio_analyzer import PortfolioAnalyzer

class Sharpes_Analyzer(PortfolioAnalyzer):
    def analyze(self):
        st.write("5. Sharpe Ratio Analyzer")
        
        pass
    def graph(self):
        st.write("Portfolio Sharpes across time:")
        pass