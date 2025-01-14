import { Button, Flex, Stack, Text, Card, Group } from "@mantine/core";
import { Dropzone } from '@mantine/dropzone';
import { Upload, CheckCircle2, XCircle, FileText } from "lucide-react";
import React, {useState} from "react";

interface UploadFileProps {
    onFileLoad: (content: string) => void;
    closeModal: () => void;
  }
  


export const UploadFile: React.FC<UploadFileProps> = ({onFileLoad, closeModal}) => {
    const [error, setError] = useState<string | null>(null);
    const [file, setFile] = useState<File | null>(null);
    const [fileContent, setFileContent] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleDrop =  (files: File[]) => {
      // handle Drop from Dropzone
        const selectedFile = files[0]; //only one file
        if (selectedFile.type !== 'text/plain') {
          setError('Only text files are supported');
          setFile(null);
          return;
        }

        setFile(selectedFile);
        setError(null);
        setLoading(true);

        console.log(selectedFile);
        const reader = new FileReader();
        reader.onload = () => {
            setLoading(false);
            if (reader.result) {
                setFileContent(reader.result as string); //save file content
              }
        };

        reader.readAsText(selectedFile);
    };


    const handleSubmit = async (event: React.FormEvent) => {
      // function to handle submit (click on button)
        event.preventDefault(); // don't reload page!
        if (fileContent) {
            onFileLoad(fileContent); //load content on editor
            closeModal(); //close this object on editor
          }
      };

    return (
        <form onSubmit={handleSubmit}>
        <Stack>
            <Dropzone onDrop={handleDrop} loading={loading} multiple={false} 
            onReject={() =>{ setError('Solo se admiten archivos de texto');}} 
            accept={["text/plain"]}>
              {/* content dropzone */}
              <Flex align="center" justify="center" style={{ height:200, border: '2px dotted #ccc' }} direction="column" gap="xs">
                {file && (
                    <Card shadow="sm" padding="sm" radius="sm" withBorder>
                        <Card.Section style={{ display: 'flex', justifyContent: 'center' }}><FileText size={64} /></Card.Section>
                        <Text>{file.name}</Text>
                    </Card>
                )}
                {!loading && !file && (
                    <>
                        <Upload />
                        <Text>Arrastra un archivo o haz click para seleccionarlo</Text>
                    </>
                )}
              </Flex>
            </Dropzone>
          {/* outside dropzone */}
          <Group justify="center">
          <Button type="submit" disabled={!file}> {/* SUMBIT BUTTON */}
            Cargar archivo
          </Button>
          <Button type="button" onClick={() => { setFile(null); setFileContent(null); setError(null); }}>
            Borrar archivo
          </Button>
          </Group>

          {/* show messages for user feedback */}
          {file && (
          <Flex align="center" gap="sm">
            <CheckCircle2 color="green" />
            <Text c="green">Archivo seleccionado: {file.name}</Text>
          </Flex>
        )}
          {error && (
            <Flex align="center" gap="sm">
              <XCircle color="red" />
              <Text c="red">{error}</Text>
            </Flex>
          )}
        </Stack>
      </form>
    );
}