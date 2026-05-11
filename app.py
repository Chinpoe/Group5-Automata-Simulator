import streamlit as st
import graphviz

#****************
#DFA Dictionaries
#****************

dfa1 = {
    "states": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'],
    "alphabet": ['a', 'b'],
    "start_state": 'A',
    "accept_states": ['P', 'Q'],
    "transitions": {
        'A': {'a': 'B', 'b': 'B'},
        'B': {'a': 'C', 'b': 'D'},
        'C': {'a': 'E', 'b': 'D'},
        'D': {'a': 'C', 'b': 'F'},
        'E': {'a': 'I', 'b': 'H'},
        'F': {'a': 'G', 'b': 'J'},
        'G': {'a': 'E', 'b': 'K'},
        'H': {'a': 'K', 'b': 'F'},
        'I': {'a': 'I', 'b': 'K'},
        'J': {'a': 'K', 'b': 'J'},
        'K': {'a': 'L', 'b': 'M'},
        'L': {'a': 'L', 'b': 'N'},
        'M': {'a': 'O', 'b': 'M'},
        'N': {'a': 'P', 'b': 'M'},
        'O': {'a': 'Q', 'b': 'N'},
        'P': {'a': 'Q', 'b': 'N'},
        'Q': {'a': 'L', 'b': 'N'}
    }
}

dfa2 = {
    "states": ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'T'],
    "alphabet": ['0', '1'],
    "start_state": 'q1',
    "accept_states": ['q12', 'q13', 'q14', 'q15', 'q17'],
    "transitions": {
        'q1':  {'0': 'q2',  '1': 'q3'},
        'q2':  {'0': 'q4',  '1': 'T'},
        'q3':  {'0': 'T',   '1': 'q4'},
        'q4':  {'0': 'q5',  '1': 'q6'},
        'q5':  {'0': 'q5',  '1': 'q7'},
        'q6':  {'0': 'q5',  '1': 'q8'},
        'q7':  {'0': 'q9',  '1': 'q10'},
        'q8':  {'0': 'q5',  '1': 'q11'},
        'q9':  {'0': 'q12', '1': 'q13'},
        'q10': {'0': 'q14', '1': 'q15'},
        'q11': {'0': 'q9',  '1': 'q16'},
        'q12': {'0': 'q12', '1': 'q13'},
        'q13': {'0': 'q9',  '1': 'q17'},
        'q14': {'0': 'q5', '1': 'q7'},
        'q15': {'0': 'q12', '1': 'q15'},
        'q16': {'0': 'q12', '1': 'q15'},
        'q17': {'0': 'q14',  '1': 'q15'},
        'T':   {'0': 'T',   '1': 'T'}
    }
}

#**************
#DFA Checker
#**************

def run_dfa(input_string, dfa):
    #checks for the starting state
    current_state = dfa["start_state"]

    path_taken = [current_state]

    for char in input_string:
        if char not in dfa["alphabet"]:
            return False, path_taken, f"Invalid! String '{char}' is not part of the alphabet!"
    

    for char in input_string:
        if char in dfa["transitions"][current_state]:
            current_state = dfa["transitions"][current_state][char]
            path_taken.append(current_state)
        else:
            return False, path_taken, f"Invalid! String '{char}' is not part of the alphabet!"
    
    if path_taken[-1] in dfa["accept_states"]:
        return True, path_taken, f"Accepted! '{input_string}' is an accepted string!"
    else:
            return False, path_taken, f"Invalid! Ended on state {current_state}, which is not an accept state."  

#**************
# DFA Grapher
#**************

def draw_graph(dfa, path_history = None):

    dot = graphviz.Digraph(graph_attr={'rankdir': 'UD'})

    if path_history is None:
        path_history = []

    # The 'current_state' is simply the last item in our history list
    if len(path_history) > 0:
        current_state = path_history[-1] 
    else:
        current_state = None
    
    visited_states = set(path_history)


    for state in dfa["states"]:
       
        if state in dfa["accept_states"]:
            shape = 'doublecircle' 
        else:
            shape = 'circle'
        
        if state == current_state:
            # The EXACT state we are standing on right now (Dark Blue)
            dot.node(state, shape=shape, style='filled', fillcolor='#4B8BBE', fontcolor='white')
        elif state in visited_states:
            # A state we walked through previously (Light Blue Trail)
            dot.node(state, shape=shape, style='filled', fillcolor='#B0E0E6')
        else:
            # Unvisited state (Boring transparent circle)
            dot.node(state, shape=shape)

    visited_edges = []
    for i in range(len(path_history) - 1):
        visited_edges.append((path_history[i], path_history[i+1]))
    
    active_edge = visited_edges[-1] if len(visited_edges) > 0 else None


    for from_state in dfa["transitions"]:
        for char in dfa["transitions"][from_state]:
            to_state = dfa["transitions"][from_state][char]
            
            # Highlight the arrows based on our history
            if (from_state, to_state) == active_edge:
                # The exact arrow we JUST crossed
                dot.edge(from_state, to_state, label=char, color='#4B8BBE', penwidth='3', fontcolor='#4B8BBE')
            elif (from_state, to_state) in visited_edges:
                # An arrow we crossed earlier in the timeline
                dot.edge(from_state, to_state, label=char, color='#B0E0E6', penwidth='2')
            else:
                # Untouched arrows
                dot.edge(from_state, to_state, label=char)
                
    return dot



#***************
#System UI
#***************
st.title("Group 5 Automata DFA, CFG, and PDA Simulator")

st.divider()

st.header("Deterministic Finite Automaton (DFA)")
st.write("Regex 1: (a + b) (a + b)* (aa + bb) (ab + ba) (a + b)* (aba + baa)")
st.write("Regex 2: (11 + 00) (1 + 0)* (101 + 111 + 01) (00* + 11*) (1 + 0 + 11)")

user_input = st.text_input("Enter a string to test:")

choice = st.radio("Select Regex", ["Regex 1", "Regex 2"], horizontal=True)


if choice == "Regex 1":
    regex = dfa1 
else:
    regex = dfa2

# saves the current decision in memory to avoid streamlit quirk
# acts like dictionary
if 'current_choice' not in st.session_state or st.session_state['current_choice'] != choice:
    st.session_state.pop('path', None)
    st.session_state['current_choice'] = choice

#button logic 
if st.button("Run Simulation"):  
    valid, path, message = run_dfa(user_input, regex)
    
    # Save the results to memory
    st.session_state['path'] = path  
    st.session_state['message'] = message
    st.session_state['valid'] = valid
    
    # forces the page to refresh instantly so the slider appears immediately
    st.rerun()

# DISPLAY LOGIC

st.markdown("---")

# If we HAVE a path in memory, show the Interactive Trace Player
if 'path' in st.session_state:
    path = st.session_state['path']
    
    # Print the Success/Error Message
    if st.session_state['valid']:
        st.success(st.session_state['message'])
    else:
        st.error(st.session_state['message'])
        
    st.write(f"**Full Path Taken:** {path}")
    
    # The Timeline Slider
    max_steps = len(path) - 1

    if max_steps > 0:
        step = st.slider("Timeline Step", min_value=0, max_value=max_steps, value=0)
    else:
        # If empty string or instant fail, lock the step to 0 and hide the slider
        step = 0
        st.info("No transitions made. Displaying final state.")
    
    # SLICING THE LIST: We grab the history from the start up to the current slider step
    current_history = path[:step + 1]
    
    # Draw the graph with the breadcrumb trail
    st.graphviz_chart(draw_graph(regex, path_history=current_history))

# If we DO NOT have a path yet, just show the blank map
else:
    st.write("### Interactive DFA")
    st.graphviz_chart(draw_graph(regex))

st.divider()

st.header("Context-Free Grammar (CFG)")
cfg1 = {
    "S": ["ABCDBF"],
    "A": ["a", "b"],
    "B": ["Λ", "aB", "bB"],
    "C": ["aa", "bb"],
    "D": ["ab", "ba"],
    "F": ["aba", "baa"]
}


cfg2 = {
    "S": ["ABCDF"],
    "A": ["11", "00"],
    "B": ["Λ", "0B", "1B"],
    "C": ["101", "111", "01"],
    "D": ["0A", "1B"],
    "X": ["0X", "Λ"],
    "Y": ["1Y", "Λ"],
    "F": ["1", "0", "11"]
}

# 1. Figure out which CFG to show based on the radio button
if choice == "Regex 1":
    active_cfg = cfg1 
else:
    active_cfg = cfg2

st.write("Here is the formal grammar for the selected language:")

for variable, rules in active_cfg.items():
    right_side = " | ".join(rules)
    
    st.markdown(f"**{variable}** &rarr; {right_side}")

st.divider()

st.header("Pushdown Automaton (PDA)")

if choice == "Regex 1":
    st.write("Below is the structural flowchart for the PDA corresponding to Regex 1:")
    st.image("PDA-Reg1.drawio.png", caption="Regex 1: Pushdown Automaton")
else:
    st.write("Below is the structural flowchart for the PDA corresponding to Regex 2:")
    st.image("PDA-Reg2.drawio.png", caption="Regex 2: Pushdown Automaton")
