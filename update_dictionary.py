import csv

def update_dictionary():
    # Read the existing dictionary file
    with open('stock_dictionary.js', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the split points
    # Start of A-share section (after Indices)
    start_idx = -1
    for i, line in enumerate(lines):
        if "CN - A股热门" in line:
            start_idx = i
            break
    
    # Start of HK section
    end_idx = -1
    for i, line in enumerate(lines):
        if "HK - 港股热门" in line:
            end_idx = i
            break

    if start_idx == -1 or end_idx == -1:
        print("Could not find split points in stock_dictionary.js")
        return

    # Read the new A-share list
    new_stocks = []
    # Use utf-8-sig to handle potential BOM
    with open('all_stocks.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        # Print fieldnames for debugging
        print(f"CSV Fieldnames: {reader.fieldnames}")
        
        for row in reader:
            # Strip whitespace from keys just in case
            row = {k.strip(): v for k, v in row.items()}
            
            if 'code' not in row:
                print("Key 'code' not found in row:", row)
                continue
                
            # Format: { code: "600519.SH", name: "贵州茅台", region: "cn" },
            code = row['code']
            name = row['name']
            # Escape quotes in name just in case
            name = name.replace('"', '\\"')
            line = f'    {{ code: "{code}", name: "{name}", region: "cn" }},\n'
            new_stocks.append(line)

    # Construct the new content
    # Keep lines before start_idx (Indices)
    # Add a header for A-shares
    # Add new stocks
    # Keep lines from end_idx to the end (HK and US)

    new_content = lines[:start_idx]
    new_content.append('    // ==================== CN - A股全集 ====================\n')
    new_content.extend(new_stocks)
    new_content.append('\n') # Add a newline before HK section
    new_content.extend(lines[end_idx:])

    # Write back to file
    with open('stock_dictionary.js', 'w', encoding='utf-8') as f:
        f.writelines(new_content)
    
    print(f"Updated stock_dictionary.js with {len(new_stocks)} A-share stocks.")

if __name__ == "__main__":
    update_dictionary()
