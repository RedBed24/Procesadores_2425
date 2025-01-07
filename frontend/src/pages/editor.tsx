import { Container, Textarea, Title, Button, Divider, Group, Stack, Skeleton, ActionIcon, Modal, Alert, Text } from '@mantine/core';
import { useState } from 'react';
import { AbcPlayer } from '../components/abcPlayer';
import { Download, Eraser, Paperclip, SendHorizontal, Ban } from 'lucide-react';
import { UploadFile } from '../components/upload-file';
import Editor from '@monaco-editor/react';


export const EditorPartitune: React.FC = () => {
  const [musicText, setMusicText] = useState<string>(''); //text from textarea
  const [error, setError] = useState<string | null>(null);
  const [abcMusic, setAbcMusic] = useState<string>(''); //abc text from backend
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [uploadModalOpened, setUploadModalOpened] = useState<boolean>(false);

  const handleSubmit = async () => {
    setError(null);
    try {
      if (!musicText) {
        throw new Error('No hay texto, no se puede enviar.');
      }
      const formData = new FormData();
      const abcBlob = new Blob([musicText], { type: 'text/plain' });
      formData.append('file', abcBlob, 'music.abc');

      const response = await fetch('/generate_abc', { //send to backend
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      // get response as JSON
      const data = await response.json();
      const text = data.content;

      setAbcMusic(text);
      setIsSubmitted(true);

    } catch (err: any) {
      setError(err.message || 'Error al generar el archivo');
    }
  };

  const downloadText = () => {
    // download abc music
    const file = new Blob([abcMusic], { type: 'text/plain' });
    const url = URL.createObjectURL(file);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'music.txt'; // Poner un nombre al archivo
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleFileLoad = (content: string) => {
    // from subir archivo
    setMusicText(content);
  };

  return (
    <>
      <Container size='xl' fluid>
        <Stack>
          <Text
            ta="center"
            mb="md"
            fz={40}
            fw={900}
            style={{
              fontFamily: 'Trebuchet MS',
              fontStyle: 'sans-serif',
              textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
            }}
          >
            🎵 Música en lenguaje PartiTune 🎶
          </Text>
          {/* <Textarea placeholder="Escribe aquí tu música"
            autosize
            minRows={15}
            maxRows={15}
            value={musicText}
            onChange={(event) => setMusicText(event.currentTarget.value)}
          /> */}
          <Editor
      height="300px" 
      defaultLanguage="plaintext"
      value={musicText}
      onChange={(newValue) => setMusicText(newValue || "")}
      options={{
        minimap: { enabled: false },
        lineNumbers: "on",
        scrollBeyondLastLine: false, 
        wordWrap: "on", 
      }}
    />
          <Group>
            <Button mt='xl' size='md' onClick={handleSubmit} rightSection={<SendHorizontal />}>
              Convertir
            </Button>
            <Button mt='xl' size='md' onClick={() => { setMusicText(''); setIsSubmitted(false); }} rightSection={<Eraser />}>
              Borrar
            </Button>
            <Button mt='xl' size='md' onClick={() => { setUploadModalOpened(true); }} rightSection={<Paperclip />}>
              Subir archivo
            </Button>
          </Group>
        </Stack>
        {error &&
          <Alert mt='sm' variant='filled' color='red' title='Error' radius='md' icon={<Ban />}>{error}</Alert>
        }
        <Divider my='xl' />

        {/* Apartado Texto musica ABC */}

        <Group align="stretch" justify="flex-start" mb='xl'>
          <Stack w='45%' mt='xl' align="stretch"
            justify="flex-start" mr='xl'>
            <Title order={2} ta="center" mb="md" size={30} style={{ fontFamily: 'Trebuchet MS', fontStyle: 'sans-serif' }} >
              Música ABC
            </Title>
            {isSubmitted && (<Stack style={{ position: 'relative' }}>
              <ActionIcon onClick={downloadText}
                style={{
                  height: '24px',
                  padding: '0 5px',
                  borderRadius: '3px',
                  margin: 0,
                  position: 'absolute',
                  top: '-10px',
                  right: '0px',
                  zIndex: 1
                }}><Download /></ActionIcon>
              <Textarea description='Música en formato ABC' readOnly autosize
                minRows={20}
                maxRows={20}
                value={abcMusic}
                styles={{ description: { color: 'black' } }}
              />
            </Stack>)}

          </Stack>
          {/* Apartado de reproduccion */}

          <Stack w='47%' mt='xl' align="stretch" gap='xs'
            justify="flex-start">
            <Title order={2} ta="center" mb="md" size={30} style={{ fontFamily: 'Trebuchet MS', fontStyle: 'sans-serif' }}>
              Partitura y Audio
            </Title>
            {isSubmitted && (<AbcPlayer abcMusic={abcMusic} display={isSubmitted} />)}
          </Stack>
        </Group>

        {/* Modal */}
        <Modal opened={uploadModalOpened} onClose={() => setUploadModalOpened(false)} size="lg">
          <UploadFile onFileLoad={handleFileLoad} closeModal={() => setUploadModalOpened(false)} />
        </Modal>


      </Container>
    </>
  )
}

