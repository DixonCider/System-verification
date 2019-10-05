import random, os, datetime

def get_state_from_level(states_level_map, level):
  return random.choice(states_level_map[level])

def generate_states_level_map(n_states, n_faulty_levels):
  st_lev_map = dict()

  for state in range(n_states):
    lev_of_state = random.randint(0, n_faulty_levels-1)

    if st_lev_map.get(lev_of_state) is not None:
      st_lev_map[lev_of_state].append(state)
    else:
      st_lev_map[lev_of_state] = [state]

  assert len(st_lev_map) == n_faulty_levels, \
    'Some levels are not populated, try increase number of states or decrease number of faulty levels'

  return st_lev_map

def adjust_jump_bounds(current_level, n_faulty_levels, jump_lower_bound, jump_upper_bound, inp):
  if inp == '0':
    if (current_level - jump_lower_bound) < 0:
      return 0, 0
    elif (current_level - jump_upper_bound) < 0:
      return 0, (current_level - jump_lower_bound)
    else:
      return (current_level - jump_upper_bound), (current_level - jump_lower_bound)

  elif inp == '1':
    if (current_level + jump_lower_bound) >= n_faulty_levels:
      return (n_faulty_levels - 1), (n_faulty_levels - 1)
    elif (current_level + jump_upper_bound) >= n_faulty_levels:
      return (current_level + jump_lower_bound), (n_faulty_levels - 1)
    else:
      return (current_level + jump_lower_bound), (current_level + jump_upper_bound)

def generate_transitions(n_states, n_faulty_levels, states_level_map, jump_lower_bound, jump_upper_bound):
  transitions = [ [-1, -1] for x in range(n_states) ]

  for level in sorted(states_level_map.keys()):
    zero_lower_bound, zero_upper_bound = adjust_jump_bounds(level, n_faulty_levels, jump_lower_bound, jump_upper_bound, '0')
    one_lower_bound, one_upper_bound = adjust_jump_bounds(level, n_faulty_levels, jump_lower_bound, jump_upper_bound, '1')
    
    # print ('level {}:'.format(level))
    # print ('zero: {} {}'.format(zero_lower_bound, zero_upper_bound))
    # print ('one:  {} {}'.format(one_lower_bound, one_upper_bound))

    for state in states_level_map[ level ]:
      zero_transition_level = random.randint(zero_lower_bound, zero_upper_bound)
      one_transition_level = random.randint(one_lower_bound, one_upper_bound)

      # print ('state: {}, 0 -- {} ; 1 -- {}'.format(state, zero_transition_level, one_transition_level))

      transitions[state][0] = get_state_from_level(states_level_map, zero_transition_level)
      transitions[state][1] = get_state_from_level(states_level_map, one_transition_level)  

  return transitions

def assign_unsafe_states(n_states, unsafe_fraction, states_level_map):
  n_unsafe_states = int(unsafe_fraction * n_states)
  current_unsafe_cnt = 0

  states_unsafe_list = [0 for x in range(n_states)]

  for level in sorted(states_level_map.keys(), reverse=True):
    unsafe_states_left = n_unsafe_states - current_unsafe_cnt

    if unsafe_states_left < len(states_level_map[level]):
      last_level_unsafe_states = random.sample(states_level_map[level], unsafe_states_left)

      for state in last_level_unsafe_states:
        states_unsafe_list[state] = 1

      break

    for state in states_level_map[level]:
      states_unsafe_list[state] = 1

    current_unsafe_cnt += len(states_level_map[level])

    # print ('level:', level)
    # print ('unsafe left:', n_unsafe_states - current_unsafe_cnt)

  return states_unsafe_list

def generate_automaton(n_states, n_faulty_levels, unsafe_fraction, jump_lower_bound, jump_upper_bound):
  assert n_states > 0, 'Please give a positive number of states'

  assert n_faulty_levels > 0, 'Please give a positive number of faulty levels'

  assert n_faulty_levels < n_states, 'Please give less faulty levels, or more states'

  assert unsafe_fraction >= 0.0 and unsafe_fraction <= 1.0, 'Please give a value between 0~1 for fraction of unsafe states'

  assert jump_lower_bound >= 0, 'Please give 0 or a positive lower bound of jump levels'

  assert jump_upper_bound >= jump_lower_bound, 'Upper bound of jump levels smaller than lower bound'

  assert jump_lower_bound < n_faulty_levels and jump_upper_bound < n_faulty_levels, \
    '''Bounds of jump levels exceed number of faulty levels.
    Please give "jump lower bound" & "jump upper bound" < "number of faulty_levels"'''

  states_level_map = generate_states_level_map(n_states, n_faulty_levels)

  print ('Faulty Level of States ---')
  for key in sorted(states_level_map.keys()):
    print (key, ':', states_level_map[key])
  print ('====================================')

  states_transitions = generate_transitions(n_states, n_faulty_levels, states_level_map, jump_lower_bound, jump_upper_bound)

  print ('State transitions on [receiving 0, receiving 1] ---')
  for i in range( len(states_transitions) ):
    print (i, ':', states_transitions[i])
  print ('====================================')

  unsafe_states_list = assign_unsafe_states(n_states, unsafe_fraction, states_level_map)

  print ('States\' Safety Status ---')
  for level in sorted(states_level_map.keys(), reverse=True):
    for state in states_level_map[level]:
      print ('state: {}, unsafe: {}'.format(state, unsafe_states_list[state]))
  print ('====================================')

  '''
  Pick an initial state from faulty level 0, and swap it with the state w/ index 0
  (i.e. make sure the initial state is State 0)
  '''
  init_state = get_state_from_level(states_level_map, 0)

  # print ('Before swap ---')
  # print (unsafe_states_list[0], unsafe_states_list[init_state])
  # print (states_transitions[0], states_transitions[init_state])

  unsafe_states_list[0], unsafe_states_list[init_state] = unsafe_states_list[init_state], unsafe_states_list[0]
  states_transitions[0], states_transitions[init_state] = states_transitions[init_state], states_transitions[0]

  # print ('After swap ---')
  # print (unsafe_states_list[0], unsafe_states_list[init_state])
  # print (states_transitions[0], states_transitions[init_state])

  return states_transitions, unsafe_states_list

def get_user_input_with_default(input_prompt, default_value): 
  ret = input(input_prompt)
  if not ret:
    ret = default_value

  return ret

def write_output(states_transitions, states_unsafe_list, n_states, n_faulty_levels, unsafe_fraction, jump_lower_bound, jump_upper_bound):
  dirname = './automata_testcases/'
  generated_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

  if not os.path.exists(dirname):
    os.mkdir(dirname)

  output_filename = '{}_NS-{}_NFL-{}_USFRAC-{}_JLB-{}_JUB-{}.txt'.format(
    generated_timestamp, n_states, n_faulty_levels, unsafe_fraction, jump_lower_bound, jump_upper_bound
  )

  # output_filename = 'a.txt'

  with open(dirname + output_filename, 'w') as f:
    f.write( '{}\n'.format(n_states) )

    for i in range(n_states):
      f.write( '{} {} {}\n'.format(states_transitions[i][0], states_transitions[i][1], states_unsafe_list[i]) )

  return

if __name__ == "__main__":
  n_states = int( get_user_input_with_default('Number of States [100]: ', 100) )  
  n_faulty_levels = int( get_user_input_with_default('Number of Faulty Levels [10]: ', 10) )  
  unsafe_fraction = float( get_user_input_with_default('Fraction of Unsafe States (0~1) [0.2]: ', .2) )  
  jump_lower_bound = int( get_user_input_with_default('Lower Bound of Jump Levels [0]: ', 0) )  
  jump_upper_bound = int( get_user_input_with_default('Upper Bound of Jump Levels [1]: ', 1) ) 

  print ('====================================')

  states_transitions, states_unsafe_list = \
    generate_automaton(
      n_states=n_states,
      n_faulty_levels=n_faulty_levels,
      unsafe_fraction=unsafe_fraction,
      jump_lower_bound=jump_lower_bound,
      jump_upper_bound=jump_upper_bound,
    )

  write_output(states_transitions, states_unsafe_list, n_states, n_faulty_levels, unsafe_fraction, jump_lower_bound, jump_upper_bound)
  