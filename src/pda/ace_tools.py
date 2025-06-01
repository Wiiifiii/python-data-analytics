# src/pda/ace_tools.py

def display_dataframe_to_user(title: str, df):
    """
    A minimal stand‐in for the PDA ace_tools display function.
    When called, it simply prints the title and DataFrame to stdout.
    If you want a richer experience, you can expand this later.
    """
    print(f"\n=== {title} ===")
    print(df)
    print()  # blank line for readability
