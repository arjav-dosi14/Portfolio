import re

def fix_hero_spacing(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The Hero section tag
    old_target = '<section id="home" class="pt-32 pb-24 bg-white relative overflow-hidden" aria-label="Hero">'
    new_target = '<section id="home" class="pt-32 pb-10 lg:pb-12 bg-white relative overflow-hidden" aria-label="Hero">'
    
    # Also in case there's any min-h-screen or items-center we should adjust it.
    # The prompt says: "Reduce the bottom whitespace by adjusting the Hero section's height, minimum height, flex alignment, or bottom padding."
    # If the user specifically mentions flex alignment, maybe they noticed `items-center` pushes the left column up, creating space at the bottom?
    # If I change items-center to items-start, the tech tags will be pushed up, creating MORE space at the bottom of the grid, which then can be reduced by pb-10. But items-center looks good for vertical balance. 
    # Let's just adjust the padding first.
    
    if old_target in content:
        content = content.replace(old_target, new_target)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Target not found in {filepath}")

fix_hero_spacing(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
fix_hero_spacing(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
