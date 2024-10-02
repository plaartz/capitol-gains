# Style Sheet 

NOTE: these style standards are mostly based on the PEP 8 standards and Airbnb javascript standards. Any code that does not fit these standards will not receive a push request approval.

## Variables
- Classes capitalized and no underscores.
    - ` class MyCoolClass: ` or ` class MyCoolClass{} `
- Booleans should be snake case with underscores and start with is_ or has_.
    - ` is_cool ` or ` has_swag `
- Everything else is snake case (underscores).
    - ` my_variable `
    - ` def my_function(): ` or ` function my_cool_function(){} `
- All dates must be in iso format.
    - ` YYYY/MM/DD H:M:S `
- Be clear with what your variable names and function names are. Avoid abbreviations.
    - ` moving_day_averge ` not ` mv_day_avg `
- Python function definitions should have type hints.
    - ` my_function(parameter_1: int, parameter_2: int) -> int: `
- Constants should be capitalized with under scores.
    - ` PI_ROUNDED = 3.14 `

## Spacing 
- Put spaces before and after operators.
    - ` x = x + 1 ` (not ` x=x+1 `)
- Use 4 spaces instead of tabs.
- The max length of lines should be 100 characters.
- One line gap between process within function.
    ```python
        def cool_function(): 
            # Code for process 1

            # Code for process 2   
    ```     
- Two line gap between functions.
    ```python 
        def add():
            # Code for add
        

        def divide():
            # Code for divide
    ```
- For JavaScript, use this bracket formatting.
    ```js
        if (something){
            // Swag code
        }else{
            // Swag code
        }
    ```
- Space after comment starts.
    ```python
        # Comment
    ```
    ``` js
        // Comment
    ```

## Logic
- `while(true)` instead of `while(1)`.
- Use `if(is_my_true_bool)` instead of `if(is_my_true_bool == true)`.

# Comments 
- Comments should be used to  provide valuable insights that are not immediately obvious from the code itself.
- Every function (besides simple constructors, setters, and getters) needs a block comment. If there are no parameters or return values, those can be left out.
    ```python 
        def my_function(parameter_1: int, parameter_2: int) -> int:
                '''
                <Function description.>

                @param parameter_1   <Description.>
                @param parameter_2   <Description.>
                @return    <Description.>

                '''
    ```  
    ```js
        /*
        * <Function description.>

        * @param {type} parameter_1 <Description.>
        * @param {type} parameter_2 <Description.>
        * @return {type} <Description.>
        */
        const function_name = (param) => {}
    ```
- Function header and comments should match above 
- Every class needs a block comment as well, in the same format as function block comments.
- Comments must start with a capital letter and end with a puncuation. 

