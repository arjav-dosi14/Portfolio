import re

def adjust_spacing(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target block for the about section wrapper and heading wrapper
    # `<div class="relative z-10 pt-8 pb-12 md:pt-10 md:pb-16 max-w-6xl mx-auto px-6 flex flex-col">`
    # `<div class="reveal mb-16 text-center flex flex-col items-center">`
    
    # 1. Reduce top padding: pt-8 md:pt-10 -> pt-4 md:pt-6
    content = content.replace(
        '<div class="relative z-10 pt-8 pb-12 md:pt-10 md:pb-16 max-w-6xl mx-auto px-6 flex flex-col">',
        '<div class="relative z-10 pt-4 pb-12 md:pt-6 md:pb-16 max-w-6xl mx-auto px-6 flex flex-col">'
    )
    
    # 2. Reduce bottom margin on the heading wrapper: mb-16 -> mb-10
    # Make sure we only replace it in the About section.
    target_heading = '''        <div class="reveal mb-16 text-center flex flex-col items-center">
            <h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">About Me</h2>'''
            
    replacement_heading = '''        <div class="reveal mb-10 text-center flex flex-col items-center">
            <h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">About Me</h2>'''
            
    content = content.replace(target_heading, replacement_heading)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated spacing in {filepath}")

adjust_spacing(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
adjust_spacing(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
