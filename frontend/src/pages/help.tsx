import { Card, Container, Flex, Title } from "@mantine/core";
import { Author } from "../components/author";

export const Help: React.FC = () => {
    return (
        <Container fluid>
          <Title order={2} ta="center" mb="md">
        Autores
          </Title>
          <Flex 
        direction={{ base: 'column', md: 'row' }} 
        justify="center" 
        align="center" 
        gap="xl"
          >
        <Author username='elena-17' />
        <Author username='redBed24' />
        <Author username='J3Burgos' />
        <Author username='Sikander035' />
          </Flex>
        </Container>
    );
}