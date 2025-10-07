#!/usr/bin/env python3

# Read the file
with open('app.py', 'r') as f:
    lines = f.readlines()

# Fix indentation issues in tab2 section
in_tab2 = False
fixed_lines = []

for i, line in enumerate(lines):
    if 'with tab2:' in line:
        in_tab2 = True
        fixed_lines.append(line)
        continue
    
    if in_tab2 and line.startswith('with tab3:'):
        in_tab2 = False
        fixed_lines.append(line)
        continue
    
    if in_tab2:
        # Fix specific indentation issues
        if line.startswith('            # Always show the trending stocks'):
            fixed_lines.append('    # Always show the trending stocks and analysis options\n')
        elif line.startswith('            # 1. Fetch 10 trending stocks'):
            fixed_lines.append('    # 1. Fetch 10 trending stocks\n')
        elif line.startswith('            trending = trending_stocks[:10]'):
            fixed_lines.append('    trending = trending_stocks[:10]\n')
        elif line.startswith('            # 2. Display all 10 trending stocks'):
            fixed_lines.append('    # 2. Display all 10 trending stocks\n')
        elif line.startswith('            df = pd.DataFrame(trending, columns=["Ticker", "Company"])'):
            fixed_lines.append('    df = pd.DataFrame(trending, columns=["Ticker", "Company"])\n')
        elif line.startswith('            st.markdown("### 🔥 Currently Trending Tickers")'):
            fixed_lines.append('    st.markdown("### 🔥 Currently Trending Tickers")\n')
        elif line.startswith('            st.dataframe(df, hide_index=True)'):
            fixed_lines.append('    st.dataframe(df, hide_index=True)\n')
        elif line.startswith('            choice = st.radio('):
            fixed_lines.append('    choice = st.radio(\n')
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write the fixed file
with open('app.py', 'w') as f:
    f.writelines(fixed_lines)

print("Fixed indentation issues in tab2")
