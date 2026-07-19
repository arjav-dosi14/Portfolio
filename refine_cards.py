import re

def refine_cards(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The cards block
    old_target = '''            <div class="pt-8 grid sm:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex items-start gap-4">
                    <svg class="w-5 h-5 text-gray-500 shrink-0 mt-0.5" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                    <div>
                        <h4 class="font-bold text-gray-800 text-sm tracking-tight mb-1">Continuous Learning</h4>
                        <p class="text-xs text-gray-500">Continuously improving skills in Python, Java, and C++.</p>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex items-start gap-4">
                    <svg class="w-5 h-5 text-gray-500 shrink-0 mt-0.5" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M13 10V3L4 14h7v7l9-11h-7z">
                        </path>
                    </svg>
                    <div>
                        <h4 class="font-bold text-gray-800 text-sm tracking-tight mb-1">Problem Solving</h4>
                        <p class="text-xs text-gray-500">Strong analytical and problem-solving skills.</p>
                    </div>
                </div>
            </div>'''
            
    # Applying the requirements:
    # 1. p-6 -> p-8 (More internal padding, increases overall height slightly)
    # 2. items-start -> items-center (Vertically center the feature icon)
    # 3. gap-4 -> gap-6 (Increase spacing between icon and text)
    # 4. remove mt-0.5 from svgs
    # 5. svg size w-5 h-5 -> w-6 h-6 to balance the increased padding (optional, but looks better, though prompt didn't say resize icons) Let's keep icons same or slightly larger? I'll keep w-6 h-6 since padding is much bigger now. Actually, user said "Do not redesign the cards", so I'll keep them w-5 h-5.
    # 6. h4 mb-1 -> mb-2 (title and description comfortable spacing)
    # 7. Add h-full to the cards to ensure they are exactly the same height if content differs.
    
    new_target = '''            <div class="pt-8 grid sm:grid-cols-2 gap-6 items-stretch">
                <div class="h-full bg-white p-8 rounded-2xl border border-gray-200 shadow-sm flex items-center gap-6">
                    <svg class="w-5 h-5 text-gray-500 shrink-0" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                    <div>
                        <h4 class="font-bold text-gray-800 text-sm tracking-tight mb-2">Continuous Learning</h4>
                        <p class="text-xs text-gray-500 leading-relaxed">Continuously improving skills in Python, Java, and C++.</p>
                    </div>
                </div>
                <div class="h-full bg-white p-8 rounded-2xl border border-gray-200 shadow-sm flex items-center gap-6">
                    <svg class="w-5 h-5 text-gray-500 shrink-0" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M13 10V3L4 14h7v7l9-11h-7z">
                        </path>
                    </svg>
                    <div>
                        <h4 class="font-bold text-gray-800 text-sm tracking-tight mb-2">Problem Solving</h4>
                        <p class="text-xs text-gray-500 leading-relaxed">Strong analytical and problem-solving skills.</p>
                    </div>
                </div>
            </div>'''
            
    if old_target in content:
        content = content.replace(old_target, new_target)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Target not found in {filepath}")

refine_cards(r'c:\Users\ARJAV\PycharmProjects\Portfolio\templates\index.html')
refine_cards(r'c:\Users\ARJAV\PycharmProjects\Portfolio\docs\index.html')
