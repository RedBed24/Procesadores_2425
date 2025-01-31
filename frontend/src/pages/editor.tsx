import { Container, Textarea, Title, Button, Divider, Group, Stack, Skeleton, ActionIcon, Modal, Alert, Text } from '@mantine/core';
import { useState } from 'react';
import React from 'react';
import { AbcPlayer } from '../components/abcPlayer';
import { Download, Eraser, Paperclip, SendHorizontal, Ban, TriangleAlert, LightbulbIcon, Lightbulb } from 'lucide-react';
import { UploadFile } from '../components/upload-file';
import Editor from '@monaco-editor/react';


export const EditorPartitune: React.FC = () => {
  const [musicText, setMusicText] = useState<string>(''); //text from textarea
  const [error, setError] = useState<string | null>(null);
  const [abcMusic, setAbcMusic] = useState<string>(''); //abc text from backend
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [uploadModalOpened, setUploadModalOpened] = useState<boolean>(false);
  const [warnings, setWarnings] = useState<string>('');

  const handleSubmit = async () => {
    setError(null);
    try {
      if (!musicText) {
        throw new Error('No hay texto, no se puede enviar.');
      }
      const formData = new FormData();
      const abcBlob = new Blob([musicText], { type: 'text/plain' });
      formData.append('file', abcBlob, 'music.abc');

      const response = await fetch('/generateABC', { //send to backend
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }
      // get response as JSON
      const data = await response.json();
      const text = data.content;
      const warnings = data.warnings;
      setAbcMusic(text);
      setWarnings(warnings);
      setIsSubmitted(true);

    } catch (err: any) {
      setError(err.message || 'Error al generar el archivo');
      setIsSubmitted(false);
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
      <Container size='xl' fluid >
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
          <Text size='sm' mb={0}>Escribe aquí la música</Text>
          <div style={{ marginTop: '0px',  borderRadius: '5px', border: '1px solid #ced4da' }}>
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
          </div>
          <Group mt='xl' justify='center'>
            <Button size='md' onClick={handleSubmit} rightSection={<SendHorizontal />}>
              Convertir
            </Button>
            <Button size='md' onClick={() => { setMusicText(''); setIsSubmitted(false); setError(''); setWarnings('')}} rightSection={<Eraser />}>
              Borrar
            </Button>
            <Button size='md' onClick={() => { setUploadModalOpened(true); }} rightSection={<Paperclip />}>
              Subir archivo
            </Button>
            <Button size='md' onClick={() => { setMusicText('obra "Titanic" {\n\
    compas = 4/4\n\
    clave = SOL\n\
    {\n\
        |:bl (fa)\n\
        c (fa fa)\n\
        n (fa mi)\n\
        bl (fa)\n\
        n (fa mi)\n\
        bl (fa)\n\
        n (sol)\n\
        bl (la sol)\n\
        bl (fa) \n\
        c (fa fa)\n\
        n (fa mi)\n\
        bl (fa)\n\
        n (fa)\n\
        r (do) :|\n\
        |: r (fa)\n\
        bl (sol.)\n\
        n (do)\n\
        bl (do\')\n\
        n (b si la)\n\
        bl (sol)\n\
        n (la b si)\n\
        bl (la)\n\
        n (sol fa mi)\n\
        bl (fa)\n\
        n (fa mi)\n\
        bl (fa)\n\
        n (sol)\n\
        bl (la)\n\
        bl (sol) :|\n\
        r (do)\n\
    }\n\
}\n\
              ') }} rightSection={<Lightbulb />}>
              Ejemplo
            </Button>
          </Group>
        </Stack>
        {error &&
          <Alert mt='sm' variant='filled' color='red' radius='md' icon={<Ban />}>
            {error.split('\n').map((line, index) => (
            <React.Fragment key={index}>
              {line}
              {index < error.split('\n').length - 1 && <br />}
            </React.Fragment>
          ))}</Alert>
        }
        {warnings &&
          <Alert
            mt="sm"
            variant="filled"
            color="orange"
            
            radius="md"
            icon={<TriangleAlert />}
          >
            {warnings.split('\n').map((line, index) => (
              <React.Fragment key={index}>
                {line}
                {index < warnings.split('\n').length - 1 && <br />}
              </React.Fragment>
            ))}
          </Alert>
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

