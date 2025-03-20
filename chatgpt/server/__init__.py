 # -*- coding: utf-8 -*-
 import re

 def filter_comments(code):
  """
  Filters out comments from a given code string.

  Args:
  code (str): The input code string.

  Returns:
  str: The code string with comments removed.
  """
  # Remove single-line comments
  code = re.sub(r'#.*', '', code)

  # Remove multi-line comments
  code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
  code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)

  return code


 def format_code(code):
  """
  Formats the code by removing extra blank lines and trailing whitespace.

  Args:
  code (str): The input code string.

  Returns:
  str: The formatted code string.
  """
  # Remove extra blank lines
  lines = code.splitlines()
  lines = [line.rstrip() for line in lines]
  lines = [line for line in lines if line]  # Remove empty lines

  return '\n'.join(lines)


 def extract_function_name(code):
  """
  Extracts the function name from a given code string.

  Args:
  code (str): The input code string containing a function definition.

  Returns:
  str: The name of the function, or None if not found.
  """
  match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
  if match:
  return match.group(1)
  else:
  return None


 def add_line_number(code):
  """
  Adds line numbers to each line of the code.

  Args:
  code (str): The input code string.

  Returns:
  str: The code string with line numbers added to each line.
  """
  lines = code.splitlines()
  numbered_lines = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
  return '\n'.join(numbered_lines)


 def modify_variable_names(code):
  """
  Modifies variable names in the code by adding a prefix.

  Args:
  code (str): The input code string.

  Returns:
  str: The modified code string with variable names prefixed.
  """

  def replace_variable(match):
  variable_name = match.group(1)
  return match.group(0).replace(variable_name, "my_var_" + variable_name)

  # Regex to find variable names (simple example, might need adjustments)
  code = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)', replace_variable, code)
  return code


 def main():
  """
  Main function to demonstrate the usage of the code processing functions.
  """
  code_example = """
  def my_function(arg1, arg2):
  # This is a single-line comment

  '''
  This is a
  multi-line comment
  '''
  result = arg1 + arg2 # Add the arguments
  return result


  \"\"\"
  Another multi-line comment
  \"\"\"
  x = 10
  y = 20
  print(x + y)
  """

  print("Original Code:\n", code_example)

  filtered_code = filter_comments(code_example)
  print("\nCode after filtering comments:\n", filtered_code)

  formatted_code = format_code(filtered_code)
  print("\nCode after formatting:\n", formatted_code)

  function_name = extract_function_name(code_example)
  print("\nExtracted Function Name:", function_name)

  numbered_code = add_line_number(formatted_code)
  print("\nCode with line numbers:\n", numbered_code)

  modified_code = modify_variable_names(code_example)
  print("\nCode with modified variables:\n", modified_code)


 if __name__ == "__main__":
  main()


 # -*- coding: utf-8 -*-
 import re

 def filter_comments(code):
  """
  Filters out comments from a given code string.

  Args:
  code (str): The input code string.

  Returns:
  str: The code string with comments removed.
  """
  # Remove single-line comments
  code = re.sub(r'#.*', '', code)

  # Remove multi-line comments
  code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
  code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)

  return code


 def format_code(code):
  """
  Formats the code by removing extra blank lines and trailing whitespace.

  Args:
  code (str): The input code string.

  Returns:
  str: The formatted code string.
  """
  # Remove extra blank lines
  lines = code.splitlines()
  lines = [line.rstrip() for line in lines]
  lines = [line for line in lines if line]  # Remove empty lines

  return '\n'.join(lines)


 def extract_function_name(code):
  """
  Extracts the function name from a given code string.

  Args:
  code (str): The input code string containing a function definition.

  Returns:
  str: The name of the function, or None if not found.
  """
  match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
  if match:
  return match.group(1)
  else:
  return None


 def add_line_number(code):
  """
  Adds line numbers to each line of the code.

  Args:
  code (str): The input code string.

  Returns:
  str: The code string with line numbers added to each line.
  """
  lines = code.splitlines()
  numbered_lines = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
  return '\n'.join(numbered_lines)


 def modify_variable_names(code):
  """
  Modifies variable names in the code by adding a prefix.

  Args:
  code (str): The input code string.

  Returns:
  str: The modified code string with variable names prefixed.
  """

  def replace_variable(match):
  variable_name = match.group(1)
  return match.group(0).replace(variable_name, "my_var_" + variable_name)

  # Regex to find variable names (simple example, might need adjustments)
  code = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)', replace_variable, code)
  return code


 def main():
  """
  Main function to demonstrate the usage of the code processing functions.
  """
  code_example = """
  def my_function(arg1, arg2):
  # This is a single-line comment

  '''
  This is a
  multi-line comment
  '''
  result = arg1 + arg2 # Add the arguments
  return result


  \"\"\"
  Another multi-line comment
  \"\"\"
  x = 10
  y = 20
  print(x + y)
  """

  print("Original Code:\n", code_example)

  filtered_code = filter_comments(code_example)
  print("\nCode after filtering comments:\n", filtered_code)

  formatted_code = format_code(filtered_code)
  print("\nCode after formatting:\n", formatted_code)

  function_name = extract_function_name(code_example)
  print("\nExtracted Function Name:", function_name)

  numbered_code = add_line_number(formatted_code)
  print("\nCode with line numbers:\n", numbered_code)

  modified_code = modify_variable_names(code_example)
  print("\nCode with modified variables:\n", modified_code)


 if __name__ == "__main__":
  main()