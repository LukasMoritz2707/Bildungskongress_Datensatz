import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def grouped_bars(df):

    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(df))
    width = 0.2

    bars1 = ax.bar(x - width, df['Gemini'], width, label='Gemini', alpha=0.8)
    bars2 = ax.bar(x, df['ChatGPT'], width, label='ChatGPT', alpha=0.8)
    bars3 = ax.bar(x + width, df['DeepSeek'], width, label='DeepSeek', alpha=0.8)
    bars4 = ax.bar(x + width + width, df['Grok'], width, label='Grok', alpha=0.8)

    ax.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('LLM Performance Comparison by Category', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(df['Category'])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 110)

    plt.tight_layout()
    plt.savefig('llm_comparison_grouped_bars.png', dpi=300)
    plt.show()

def heat_map(df):
    df = df.set_index('Category')

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.heatmap(df, annot=True, fmt='.1f', cmap='RdYlGn', vmin=50, vmax=100,
                cbar_kws={'label': 'Percentage (%)'}, ax=ax, linewidths=0.5)

    ax.set_title('LLM Performance Heatmap by Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('LLM', fontsize=12, fontweight='bold')
    ax.set_ylabel('Category', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('llm_comparison_heatmap.png', dpi=300)
    plt.show()

def line_Chart(df):
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(df['Category'], df['Gemini'], marker='o', linewidth=2, label='Gemini', markersize=8)
    ax.plot(df['Category'], df['ChatGPT'], marker='s', linewidth=2, label='ChatGPT', markersize=8)
    ax.plot(df['Category'], df['DeepSeek'], marker='^', linewidth=2, label='DeepSeek', markersize=8)
    ax.plot(df['Category'], df['Grok'], marker='^', linewidth=2, label='Grok', markersize=8)

    ax.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('LLM Performance Trends Across Categories', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(50, 105)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('llm_comparison_lines.png', dpi=300)
    plt.show()

def boxplot(df):

    fig, ax = plt.subplots(figsize=(10, 7))

    data_to_plot = [df['Gemini'], df['ChatGPT'], df['Grok'],df['DeepSeek']]
    bp = ax.boxplot(data_to_plot, label=['Gemini', 'ChatGPT', 'DeepSeek', 'Grok'], patch_artist=True)

    # Color the boxes
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#77FF77']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('LLM Performance Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(50, 105)

    plt.tight_layout()
    plt.savefig('llm_comparison_boxplot.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv("summary_percentages.csv")

    #grouped_bars(df)
    heat_map(df)
    #line_Chart(df)
    #boxplot(df)