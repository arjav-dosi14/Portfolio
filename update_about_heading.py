import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target block
    target = '''        <div class="reveal">
            <h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">About Me</h2>
            
        </div>

        <div class="reveal delay-200 space-y-6 text-gray-600 leading-relaxed text-[15px]">'''
        
    replacement = '''        <div class="reveal mb-16 text-center flex flex-col items-center col-span-full w-full">
            <h2 class="text-2xl font-bold text-gray-800 tracking-tight mb-4">About Me</h2>
            
        </div>

        <div class="md:col-start-2 reveal delay-200 space-y-6 text-gray-600 leading-relaxed text-[15px]">'''

    if target in content:
        content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Target block not found in {filepath}")

update_file(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
update_file(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
