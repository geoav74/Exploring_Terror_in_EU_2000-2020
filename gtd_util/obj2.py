'''
As neighbor countries I consider those which are:
- directly connected by land
- within 100km from each other by sea
'''

neighbors = {
    "Albania": ["Montenegro", "Kosovo", "North Macedonia", "Greece"],
    "Austria": ["Czechia", "Slovakia", "Hungary", "Slovenia", "Italy", "Switzerland", "Germany"],
    "Belarus": ["Lithuania", "Latvia", "Russia", "Ukraine", "Poland"],
    "Belgium": ["Netherlands", "Germany", "Luxembourg", "France"],
    "Bosnia and Herzegovina": ["Croatia", "Serbia", "Montenegro"],
    "Bulgaria": ["Romania", "Turkiye", "Greece", "North Macedonia", "Serbia"],
    "Croatia": ["Slovenia", "Hungary", "Serbia", "Bosnia and Herzegovina", "Montenegro"],
    "Cyprus": ["Turkiye"], # ~70km
    "Czechia": ["Poland", "Slovakia", "Austria", "Germany"],
    "Denmark": ["Norway", "Sweden", "Germany"], # ~5km from Sweden, ~60km from Norway
    "Estonia": ["Finland", "Russia", "Latvia"], # ~80km from Finland
    "Finland": ["Norway", "Russia", "Estonia", "Sweden"], # ~80km from Estonia
    "France": ["United Kingdom", "Belgium", "Luxembourg", "Germany", "Switzerland", "Italy", "Spain"], # ~35km from UK
    "Germany": ["Denmark", "Poland", "Czechia", "Austria", "Switzerland", "France", "Luxembourg", "Belgium", "Netherlands"],
    "Greece": ["Albania", "North Macedonia", "Bulgaria", "Turkiye"],
    "Hungary": ["Slovakia", "Ukraine", "Romania", "Serbia", "Croatia", "Slovenia", "Austria"],
    "Iceland": [],
    "Ireland": ["United Kingdom"],
    "Italy": ["Switzerland", "Austria", "Slovenia", "Croatia", "Albania", "Malta", "France"], # ~80km from Malta
    "Kosovo": ["Serbia", "North Macedonia", "Albania", "Montenegro"],
    "Latvia": ["Estonia", "Russia", "Belarus", "Lithuania"],
    "Lithuania": ["Latvia", "Belarus", "Poland", "Russia"],
    "Malta": ["Italy"], # ~80km from Italy
    "Moldova": ["Ukraine", "Romania"],
    "Montenegro": ["Bosnia and Herzegovina", "Serbia", "Kosovo", "Albania", "Croatia"],
    "Netherlands": ["Germany", "Belgium"],
    "North Macedonia": ["Serbia", "Kosovo", "Bulgaria", "Greece", "Albania"],
    "Norway": ["Russia", "Finland", "Sweden", "Denmark"], # ~60km from Denmark
    "Poland": ["Russia", "Lithuania", "Belarus", "Ukraine", "Slovakia", "Czechia", "Germany"],
    "Portugal": ["Spain"],
    "Romania": ["Ukraine", "Moldova", "Bulgaria", "Serbia", "Hungary"],
    "Russia": ["Ukraine", "Belarus", "Latvia", "Estonia", "Finland", "Norway", "Lithuania", "Poland"],
    "Serbia": ["Hungary", "Romania", "Bulgaria", "North Macedonia", "Kosovo", "Montenegro", "Bosnia and Herzegovina", "Croatia"],
    "Slovakia": ["Poland", "Ukraine", "Hungary", "Austria", "Czechia"],
    "Slovenia": ["Austria", "Hungary", "Croatia", "Italy"],
    "Spain": ["France", "Portugal"],
    "Sweden": ["Norway", "Finland", "Denmark"], # ~5km from Denmark
    "Switzerland": ["Germany", "Austria", "Italy", "France"],
    "Turkiye": ["Cyprus", "Greece", "Bulgaria"], # ~70km from Cyprus
    "Ukraine": ["Belarus", "Russia", "Moldova", "Romania", "Hungary", "Slovakia", "Poland"],
    "United Kingdom": ["France", "Ireland"], # ~35km from France
}