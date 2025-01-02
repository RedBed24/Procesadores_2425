import { Container, Textarea, Title, Button, Divider, Group, Stack, Skeleton, ActionIcon, Modal, Alert } from '@mantine/core';
import { useState } from 'react';
import { AbcPlayer } from '../components/abcPlayer';
import { Download, Eraser, Paperclip, SendHorizontal, Ban } from 'lucide-react';
import { UploadFile } from '../components/upload-file';

export const Editor: React.FC = () => {
  const [musicText, setMusicText] = useState<string>('');
  const [error, setError] = useState<string | null>(null); // Estado de errores
  const [abcMusic, setAbcMusic] = useState<string>('');
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [uploadModalOpened, setUploadModalOpened] = useState<boolean>(false);

  const handleSubmit = async () => {
    setError(null);
    try {
      if (!musicText) {
        throw new Error('No hay texto para enviar');
      }
      const formData = new FormData();
      const abcBlob = new Blob([musicText], { type: 'text/plain' });
      formData.append('file', abcBlob, 'music.abc');

      const response = await fetch('/generate_abc', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();

      const text = data.content;
      setAbcMusic(text);
      setIsSubmitted(true);

    } catch (err: any) {
      setError(err.message || 'Error al generar el archivo');
    }
  };

  const downloadText = () => {
    const file = new Blob([abcMusic], { type: 'text/plain' });
    const url = URL.createObjectURL(file);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'music.txt'; // Poner un nombre al archivo
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleFileLoad = (content: string) => {
    setMusicText(content);
  };

  return (
    <>
      <Container size='xl' fluid>
        <Stack>
          <Title order={2} ta="center" mb="md" size={30}>
            Música en lenguaje Partitune
          </Title>
          <Textarea placeholder="Escribe aquí tu música"
            autosize
            minRows={15}
            maxRows={15}
            value={musicText}
            onChange={(event) => setMusicText(event.currentTarget.value)}
          />
          <Group>
            <Button mt='xl' size='md' onClick={handleSubmit} rightSection={<SendHorizontal />}>
              Enviar
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
        <Alert mt='sm' variant='light' color='red' title='Error' radius = 'md' icon={<Ban/>}>{error}</Alert>
        }
        <Divider my='xl' />

        {/* Apartado Texto musica ABC */}

        <Group align="stretch" justify="flex-start" mb='xl'>
          <Stack w='45%' mt='xl' align="stretch"
            justify="flex-start" mr='xl'>
            <Title order={2} ta="center" mb="md" size={30}>
              Música ABC
            </Title>
            <Skeleton visible={!isSubmitted} height={450}>
              <Stack style={{ position: 'relative' }}>
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
                <Textarea description='Musica en formato ABC' readOnly autosize
                  minRows={20}
                  maxRows={20}
                  value={abcMusic}
                />
              </Stack>
            </Skeleton>
          </Stack>
          {/* Apartado de reproduccion */}

          <Stack w='47%' mt='xl' align="stretch"
            justify="flex-start">
            <Title order={2} ta="center" mb="md" size={30}>
              Partitura y Audio
            </Title>
            <Skeleton visible={!isSubmitted} height={450}>
              <AbcPlayer abcMusic={abcMusic} display={isSubmitted} />
            </Skeleton>
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

