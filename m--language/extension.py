import vscode

def activate(context):
    def run_m_code():
        editor = vscode.window.active_text_editor
        document = editor.document
        
        # Get the text and run it with your interpreter
        text = document.get_text()
        output = exec(f'python path/to/m.py', input=text)
        
        # Show output in a new output channel
        output_channel = vscode.window.create_output_channel("M- Output")
        output_channel.append(output)
        output_channel.show()
    
    disposable = vscode.commands.register_command('extension.runM', run_m_code)
    context.subscriptions.append(disposable)

# Export the activate function
exports.activate = activate
