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
        const selectedFile = files[0];
        if (selectedFile.type !== 'text/plain') {
          setError('Only text files are supported');
          setFile(null);
          console.log('Only text files are supported');
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
                setFileContent(reader.result as string);
              }
        };

        reader.readAsText(selectedFile);
    };


    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault(); 
        if (fileContent) {
            onFileLoad(fileContent);
            closeModal();
          }
      };

    return (
        <form onSubmit={handleSubmit}>
        <Stack>

            <Dropzone onDrop={handleDrop} loading={loading} multiple={false} onReject={() =>{ setError('Solo se admiten archivos de texto');}} accept={["text/plain"]}>
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
          <Group justify="center">
          <Button type="submit" disabled={!file}>Cargar archivo</Button>
          <Button type="button" onClick={() => { setFile(null); setFileContent(null); setError(null); }}>Borrar archivo</Button>
          </Group>
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