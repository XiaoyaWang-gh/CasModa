from strUtils import fetch_method_chatgpt_out, delete_test_class_shell

input_str_1 = r"""
Based on the compilation error, it seems that the test case is missing a closing parenthesis ")" and a closing brace "}" for the assertArrayEquals statement. Here's the updated test case:

```java
public class ArgumentTest8 {
    
    @Test
    public void testStripBoundaryQuotes() {
        ArgumentImpl arg = new ArgumentImpl("arg1", "description", 0, 10, ',', ';', null, null, null, 1);
        String token = "\"quoted token\"";

        String result = arg.stripBoundaryQuotes(token);
        
        assertEquals("quoted token", result);
    }
}
```

Make sure to add the closing parenthesis ")" and the closing brace "}" at the end of the assertArrayEquals statement to fix the compilation errors
  
"""

output_str_1 = fetch_method_chatgpt_out(input_str_1)


input_str_2 = r"""
public class ArgumentTest8 {
    
    @Test
    public void testStripBoundaryQuotes() {
        ArgumentImpl arg = new ArgumentImpl("arg1", "description", 0, 10, ',', ';', null, null, null, 1);
        String token = "\"quoted token\"";

        String result = arg.stripBoundaryQuotes(token);
        
        assertEquals("quoted token", result);
    }
}
"""

output_str_2 = delete_test_class_shell(input_str_2)

print(output_str_1)
