# src/pda/__init__.py
from .task1 import load_data, make_freq_table
__all__ = ["load_data", "make_freq_table"]
from .task2 import plot_histogram, plot_scatter_influence_guidance, plot_scatter_time_grade
__all__.extend(["plot_histogram", "plot_scatter_influence_guidance", "plot_scatter_time_grade"])
from .task3 import plot_scatter_influence_guidance_with_regression, plot_scatter_time_grade_with_regression
__all__.extend(["plot_scatter_influence_guidance_with_regression", "plot_scatter_time_grade_with_regression"])
from .task4 import plot_scatter_influence_guidance_with_regression_and_smooth, plot_scatter_time_grade_with_regression_and_smooth
__all__.extend(["plot_scatter_influence_guidance_with_regression_and_smooth", "plot_scatter_time_grade_with_regression_and_smooth"])
from .task5 import task2_corr, task3_corr_matrix
__all__.extend(["task2_corr", "task3_corr_matrix"])

