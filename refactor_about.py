import re

def refactor_about_me(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target block we are replacing
    # Notice we remove the grid classes and the md:col-start-2 class.
    # We will wrap the text and cards in a max-w-4xl mx-auto container to center it nicely.
    
    # We need to find the entire `<section id="about"...` up to the `md:col-start-2` div
    
    pattern = r'(<section id="about" class="relative bg-slate-50" aria-label="About Me">.*?<div class="relative z-10 pt-8 pb-12 md:pt-10 md:pb-16 max-w-6xl mx-auto px-6 )grid md:grid-cols-\[240px_1fr\] lg:grid-cols-\[280px_1fr\] gap-8 lg:gap-16 items-start(">.*?<div class="reveal mb-16 text-center flex flex-col items-center col-span-full w-full">.*?<h2.*?>About Me</h2>.*?<div class="h-px w-8 bg-gray-300"></div>.*?</div>\s*<div class=")md:col-start-2 (reveal delay-200 space-y-6 text-gray-600 leading-relaxed text-\[15px\]">)'
    
    # The replacement will:
    # 1. Remove grid classes from the main wrapper, making it a regular flex/block container (like other sections).
    # 2. Keep the heading centered (it already has text-center flex flex-col items-center).
    # 3. Add max-w-4xl mx-auto to the content div so it's a centered container.
    # We remove col-span-full and w-full from the heading since it's no longer in a grid.
    
    def repl(m):
        prefix = m.group(1) # `<section ... <div class="relative ... px-6 `
        mid = m.group(2) # `"> ... <div class="reveal mb-16 ... w-full"> ... </div> \n <div class="`
        suffix = m.group(3) # `reveal delay-200 ...">`
        
        # Clean up mid (remove col-span-full and w-full)
        mid = mid.replace('col-span-full w-full', '')
        
        # We want the content div to be max-w-4xl mx-auto to center the block below the heading
        # suffix will become `max-w-4xl mx-auto ` + suffix
        return prefix + 'flex flex-col' + mid + 'max-w-4xl mx-auto ' + suffix

    new_content = re.sub(pattern, repl, content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated {filepath}")
    else:
        print(f"Failed to find match in {filepath}")

refactor_about_me(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
refactor_about_me(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
