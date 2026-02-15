import sys
import os
from babel.messages import frontend

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_translations.py [extract|init|compile|update]")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == 'extract':
        # Equivalent to: pybabel extract -F babel.cfg -k _ -o messages.pot .
        cmd = frontend.extract_messages()
        cmd.config_file = 'babel.cfg'
        cmd.keywords = '_'
        cmd.output_file = 'messages.pot'
        cmd.input_paths = ['.']
        cmd.finalize_options()
        cmd.run()
        
    elif command == 'init':
        # Equivalent to: pybabel init -i messages.pot -d app/translations -l [lang]
        if len(sys.argv) < 3:
            print("Usage: python manage_translations.py init [lang]")
            sys.exit(1)
        lang = sys.argv[2]
        cmd = frontend.init_catalog()
        cmd.input_file = 'messages.pot'
        cmd.output_dir = 'app/translations'
        cmd.locale = lang
        cmd.finalize_options()
        cmd.run()
        
    elif command == 'compile':
        # Equivalent to: pybabel compile -d app/translations
        cmd = frontend.compile_catalog()
        cmd.directory = 'app/translations'
        cmd.finalize_options()
        cmd.run()
        
    elif command == 'update':
        # Equivalent to: pybabel update -i messages.pot -d app/translations
        cmd = frontend.update_catalog()
        cmd.input_file = 'messages.pot'
        cmd.output_dir = 'app/translations'
        cmd.finalize_options()
        cmd.run()
