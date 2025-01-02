import { useEffect, useState } from "react";
import { Card, Image, Text, Anchor, Loader, Center } from "@mantine/core";

interface InterfaceAuthor {
    username: string;
}

export const Author: React.FC<InterfaceAuthor> = ({ username }) => {
    const [author, setAuthor] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAuthor = async () => {
            if (!username) {
                console.error("No username provided");
                return;
            }
            console.log(`Fetching data for username: ${username}`);
            try {
                const response = await fetch(`https://api.github.com/users/${username}`);
                if (response.ok) {
                    const data = await response.json();
                    setAuthor(data);
                    console.log(data);
                } else {
                    console.error(`Error fetching user: ${response.status}`);
                }
            } catch (error) {
                console.error(`Error fetching user: ${error}`);
            } finally {
                setLoading(false);
            }
        };

        fetchAuthor();
    }, [username]);

    if (loading) {
        return (
            <Center>
                <Loader />
            </Center>
        );
    }

    if (!author) {
        return (
            <Center>
                <Text color="red">No se encontró información del usuario.</Text>
            </Center>
        );
    }

    return (
        <Card shadow="sm" padding="lg" radius="md" withBorder w={150} h={250}>
            <Card.Section>
                <Anchor href={author.html_url} target="_blank" rel="noopener noreferrer" mt="xs">
                <Image
                    src={author.avatar_url}
                    alt={author.login}
                    fit="cover"
                    radius="md"
                    height={150}
                />
                </Anchor>
            </Card.Section>
            <Text size='lg' mt="md" ta='center' fw={700} >
                {author.name}
            </Text>
        </Card>
    );
};