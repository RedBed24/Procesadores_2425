import { useEffect, useState } from 'react';
import { Burger, Container, Group, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import classes from '../css/header.module.css';
import { Music } from 'lucide-react';
import { Link, useLocation } from 'wouter';


interface HeaderProps {
  links: { link: string; label: string }[];
}

export const Header: React.FC<HeaderProps> = ({ links }) => {
  const [opened, { toggle }] = useDisclosure(false);
  const [active, setActive] = useState('');
  const [location] = useLocation();

  const items = links.map((link) => (
    <Link
      key={link.label}
      href={link.link}
      className={classes.link}
      data-active={active === link.link || undefined}
      onClick={() => {
        setActive(link.link);
      }}
    >
      {link.label}
    </Link>
  ));

  useEffect(() => {
    setActive(location);
  }, [location]);

  return (
    <header className={classes.header}>
      <Container size="md" className={classes.inner} fluid>
        <Music size={42} color='#099CFF' />
        <Text mr='auto' style={{ fontWeight: 'bold', fontSize: 25, fontFamily: "Trebuchet MS", fontStyle: "sans-serif" }}>
          PARTITUNE</Text>
        <Group gap={5} visibleFrom="xs" mr='xl'> {/* render links */}
          {items}
        </Group>
        {/* Burger menu only for small devices */}
        <Burger opened={opened} onClick={toggle} hiddenFrom="xs" size="sm" />
      </Container>
    </header>
  );
}