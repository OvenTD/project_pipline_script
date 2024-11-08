import maya.mel as mel
import maya.cmds as cmds

class SceneExporter:
    character_objects = ["Bille_Rigging:Group", "Hero_Rigging:Group", "AnotherCharacter:Group"]
    export_path = "D:/Hijackers_UE/USD"

    def __init__(self):
        self.scene_number = None
        self.cut_number = None
        self.start_frame = None
        self.end_frame = None
        self.force_first_frame_checkbox = False
        self._extract_scene_and_cut_number()

    def export_alembic(self, character_name):
        """
        Exports specific objects of the selected character to Alembic.
        """
        alembic_objects = {
            "Hero_Rigging": [
                "Hero_Rigging:TEX_GEO_HeroBody_03",
                "Hero_Rigging:TEX_GEO_HeroHead_02",
                "Hero_Rigging:SIM"
            ],
            "Bille_Rigging": [
                "Bille_Rigging:GEO_High",
                "Bille_Rigging:GEO_NonProxy",
                "Bille_Rigging:SIM"
            ],
            "AnotherCharacter": [
                "AnotherCharacter:Body",
                "AnotherCharacter:Head",
                "AnotherCharacter:Accessories"
            ]
        }

        if character_name in alembic_objects:
            cmds.select(clear=True)
            for obj in alembic_objects[character_name]:
                if cmds.objExists(obj):
                    cmds.select(obj, add=True)
                else:
                    print(f"Object '{obj}' does not exist in the scene.")
            
            # Format scene and cut numbers with padding
            padded_scene_number = f"{int(self.scene_number):02d}"
            padded_cut_number = f"{int(self.cut_number):04d}"

            # Determine the character name without namespace for file naming
            character_short_name = character_name.split('_')[0]
            # Format the Alembic export path and file name
            output_path = f"D:/Houdini/Hijackers/{character_short_name}/Input/A_{padded_scene_number}_{padded_cut_number}_{character_short_name}_{self.start_frame}_{self.end_frame}.abc"
            
            # Check for selected objects
            selected_objects = cmds.ls(selection=True, long=True)
            if not selected_objects:
                cmds.warning("No objects selected for Alembic export.")
                return

            # Construct the `-root` arguments for each selected object
            root_paths = " ".join([f"-root {obj}" for obj in selected_objects])
            first_frame = 380
            if self.force_first_frame_checkbox is not None:
                first_frame = self.start_frame
            # Define the Alembic export command
            abc_command = (
                f'AbcExport -j "-frameRange {first_frame} {self.end_frame} -uvWrite -writeFaceSets -worldSpace '
                f'-writeUVSets -dataFormat ogawa {root_paths} -file {output_path}"'
            )

            # Execute the command
            mel.eval(abc_command)
            print(f"Alembic export completed for {character_name} from frame 380 to {self.end_frame} at {output_path}")
        else:
            print(f"No export configuration found for '{character_name}'.")

    def get_full_export_path(self):
        if self.scene_number is not None and self.cut_number is not None:
            return f"{SceneExporter.export_path}/S_{self.scene_number}/C_{self.cut_number:04d}"
        else:
            return SceneExporter.export_path

    def export_to_usd(self):
        full_export_path = self.get_full_export_path()
        cmds.sysFile(full_export_path, makeDir=True)

        for obj in SceneExporter.character_objects:
            if cmds.objExists(obj):
                usd_file_path = f"{full_export_path}/{obj.split(':')[-1]}.usd"
                cmds.select(obj)
                cmds.mayaUSDExport(file=usd_file_path, selection=True)
                print(f"Exported {obj} to {usd_file_path}")
            else:
                print(f"Object '{obj}' no longer exists in the scene.")

    def set_frame_range(self, start_frame, end_frame):
        """
        Stores the start and end frames with 10 added to each.
        """
        self.start_frame = start_frame - 10
        self.end_frame = end_frame + 10
        print(f"Start frame set to: {self.start_frame}, End frame set to: {self.end_frame}")

    def _extract_scene_and_cut_number(self):
        """
        Extracts the scene and cut number from the currently opened scene's file name.
        Assumes the file name follows a format like 'LO_04-04_0010_Animation_v0005.ma'.
        """
        file_name = cmds.file(query=True, sceneName=True, shortName=True)
        if file_name:
            parts = file_name.split('_')
            if len(parts) >= 3:
                # Extract and convert scene and cut numbers to integers for formatting
                self.scene_number = parts[1].split('-')[0].zfill(2)  # Pads to 2 digits
                self.cut_number = parts[2].zfill(4)    # Pads to 4 digits
            else:
                cmds.warning("File name format is not valid for extracting scene and cut numbers.")
        else:
            cmds.warning("No file is currently open.")

class SceneExporterUI:
    def __init__(self, exporter):
        self.exporter = exporter
        self.window = "sceneExporterWindow"

    def create_ui(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title="Scene Exporter", widthHeight=(300, 450))
        cmds.columnLayout(adjustableColumn=True)

        # Scene and Cut Number UI with intFields
        self.scene_label = cmds.text(label=f"Scene Number: {self.exporter.scene_number}")
        self.scene_intfield = cmds.intField(value=int(self.exporter.scene_number), minValue=1)
        
        self.cut_label = cmds.text(label=f"Cut Number: {self.exporter.cut_number}")
        self.cut_intfield = cmds.intField(value=int(self.exporter.cut_number), minValue=1)

        # Start and End Frame UI with intFields
        cmds.text(label="Start Frame:")
        self.start_frame_field = cmds.intField(value=500)
        
        cmds.text(label="End Frame:")
        self.end_frame_field = cmds.intField(value=550)

        # Force First Frame Checkbox
        self.force_first_frame_checkbox = cmds.checkBox(label="Force First Frame", value=False)

        # Update Button
        cmds.button(label="Update Scene and Cut Numbers", command=self.update_scene_and_cut_number)

        # Character Objects Scroll List
        cmds.text(label="Character Objects:")
        self.character_scroll_list = cmds.textScrollList(numberOfRows=8)

        # Export to USD Button
        #cmds.button(label="Export to USD", command=self.export_to_usd)
        
        # Alembic Export Button
        cmds.button(label="Export Alembic for Selected Character", command=self.export_selected_alembic)

        cmds.showWindow(self.window)

    def update_scene_and_cut_number(self, *args):
        # Update the scene and cut number based on the user input
        self.exporter.scene_number = cmds.intField(self.scene_intfield, query=True, value=True)
        self.exporter.cut_number = cmds.intField(self.cut_intfield, query=True, value=True)
        
        # Update labels to reflect new values
        cmds.text(self.scene_label, edit=True, label=f"Scene Number: {self.exporter.scene_number}")
        cmds.text(self.cut_label, edit=True, label=f"Cut Number: {self.exporter.cut_number}")
        
        # Refresh the character objects list
        self.update_character_objects_list()

    def update_character_objects_list(self):
        existing_objects = self.get_existing_objects()
        cmds.textScrollList(self.character_scroll_list, edit=True, removeAll=True)
        cmds.textScrollList(self.character_scroll_list, edit=True, append=existing_objects)

    def get_existing_objects(self):
        existing_objects = []
        for obj in SceneExporter.character_objects:
            if cmds.objExists(obj):
                existing_objects.append(obj)
        return existing_objects

    def export_to_usd(self, *args):
        self.exporter.export_to_usd()

    def export_selected_alembic(self, *args):
        selected_character = cmds.textScrollList(self.character_scroll_list, query=True, selectItem=True)
        if selected_character:
            character_name = selected_character[0].split(":")[0]
            start_frame = cmds.intField(self.start_frame_field, query=True, value=True)
            end_frame = cmds.intField(self.end_frame_field, query=True, value=True)
            self.exporter.set_frame_range(start_frame, end_frame)  # Store the frame range
            self.exporter.export_alembic(character_name)
        else:
            cmds.warning("Please select a character for Alembic export.")

# Usage
exporter = SceneExporter()
ui = SceneExporterUI(exporter)
ui.create_ui()
