import re

def restore_about_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target block:
    # <div class="relative z-10 pt-4 pb-12 md:pt-6 md:pb-16 max-w-6xl mx-auto px-6 flex flex-col">
    #     <div class="reveal mb-10 text-center flex flex-col items-center">
    #         <h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">About Me</h2>
    #         <div class="h-px w-8 bg-gray-300"></div>
    #     </div>
    #
    #     <div class="max-w-4xl mx-auto reveal delay-200 space-y-6 text-gray-600 leading-relaxed text-[15px]">

    pattern = r'(<div class="relative z-10 pt-4 pb-12 md:pt-6 md:pb-16 max-w-6xl mx-auto px-6 )flex flex-col(">.*?<div class="reveal) mb-10 text-center flex flex-col items-center(">.*?<h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">About Me</h2>.*?<div class="h-px w-8 bg-gray-300"></div>.*?</div>.*?<div class=")max-w-4xl mx-auto (reveal delay-200 space-y-6 text-gray-600 leading-relaxed text-\[15px\]">)'
    
    # We replace with the grid classes we used originally for the left-aligned layout.
    def repl(m):
        prefix = m.group(1)
        grid_classes = "grid md:grid-cols-[240px_1fr] lg:grid-cols-[280px_1fr] gap-8 lg:gap-16 items-start"
        reveal = m.group(2)
        end_reveal = m.group(3)
        div_start = m.group(4)
        suffix = m.group(5)
        
        return prefix + grid_classes + reveal + end_reveal + '\n        ' + div_start + suffix

    new_content = re.sub(pattern, repl, content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully restored layout in {filepath}")
    else:
        print(f"Failed to find match in {filepath}")

restore_about_layout(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
restore_about_layout(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
