from django.core.management.base import BaseCommand
from django.core.management import call_command

from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = os.path.join(BASE_DIR, "config")
VULNDB_DIR = os.path.join(CONFIG_DIR, "vulndb") 

            
class Command(BaseCommand):
    help = 'Loads finding templates to model'
    
    def read_ref_file(self, file_path):
        """Reads a Markdown file and returns its content as a string."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    def read_json_file(self, file_path):
        """Reads a JSON file and returns its content."""
        with open(file_path, 'r') as file:
            return json.load(file)
    
    def resolve_ref(self, ref):
        """Resolves a $ref to actual content by reading the referenced JSON file."""
        parts = ref.split('/')
        if len(parts) == 4 and parts[0] == '#' and parts[1] == 'files':
            directory, filename = parts[2], f"{parts[3]}.md"
            ref_file_path = os.path.join(VULNDB_DIR, directory, filename)
            try:
                return self.read_ref_file(ref_file_path)  
            except FileNotFoundError:
                print(f"File not found: {ref_file_path}")
                return None
        return None
    
    def process_vulnerability_file(self, file_path):
        """Processes a single vulnerability JSON file."""
        data = self.read_json_file(file_path)
        
        # Resolve description $ref
        if "$ref" in data["description"]:
            data["description"] = self.resolve_ref(data["description"]["$ref"])  
        
        # Resolve fix guidance $ref
        if "$ref" in data["fix"]["guidance"]:
            data["fix"]["guidance"] = self.resolve_ref(data["fix"]["guidance"]["$ref"])
            
        guidance_text = data.get("fix", {}).get("guidance", "")
        data["recommendation"] = guidance_text 
            
        data["references"] = [ref.get("url") for ref in data.get("references", [])]
        reference_string = ""
        for reference in data["references"]:
            reference_string += f"- {reference}\n"
        data["references"] = reference_string
        
        data["severity"] = data["severity"].capitalize()
        if data["severity"] == "Informational":
            data["severity"] = "Info"
            
        if 'cwe' in data and data['cwe']:
            data['cwe'] = int(data['cwe'][0])
        else:
            data['cwe'] = "0"
        
        # Remove tags (if needed)
        data.pop('tags', None)
        data.pop('id', None)
        data.pop("fix", None)
        data.pop("owasp_top_10", None)
        
        return data
    
    def compile_vulnerabilities(self, files):
        """Compiles processed vulnerabilities into the desired format."""
        vulnerabilities_compiled = []
        # pk = 1  # Starting primary key, assuming it increments for each vulnerability
        # print(int(file.name.split("-")[0]))
        i=0
        for file in files:
            # if i == 2:
            #     break
            # file_path = os.path.join(VULNDB_DIR, file)
            vulnerability_data = self.process_vulnerability_file(file)
            pk = int(file.name.split("-")[0])
            # Transform and save the processed data into the desired format
            formatted_vulnerability = {
                "model": "reporting.finding_template",
                "pk": pk,
                "fields": vulnerability_data
            }
            
            vulnerabilities_compiled.append(formatted_vulnerability)
            i+=1
        
        return vulnerabilities_compiled
        
    def handle(self, *args, **options):
        files = [f for f in Path(VULNDB_DIR).iterdir() if f.is_file()]
        vulnerabilities = self.compile_vulnerabilities(files)
        temp_filename = 'temp_vulnerabilities.json'
        
        with open(temp_filename, 'w') as outfile:
            json.dump(vulnerabilities, outfile, indent=4)
        
        call_command('loaddata', temp_filename)
        
        os.remove(temp_filename)