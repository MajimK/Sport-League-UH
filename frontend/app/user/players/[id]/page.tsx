'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Container, Card } from 'react-bootstrap';

interface Player {
    player_id: number;
    name: string;
    CI: string;
    faculty: string;
    age: number;
    email: string;
    phone: string;
    team: string;
}

// Datos de ejemplo
const samplePlayers: Player[] = [
    { player_id: 1, name: 'Juan Pérez', CI: '12345678', faculty: 'Contabilidad', age: 21, email: 'juan@example.com', phone: '555-1234', team: 'Los Halcones' },
    { player_id: 2, name: 'Ana Gómez', CI: '87654321', faculty: 'Informática', age: 22, email: 'ana@example.com', phone: '555-5678', team: 'Las Águilas' },
    { player_id: 3, name: 'Carlos Díaz', CI: '11223344', faculty: 'Matemática', age: 23, email: 'carlos@example.com', phone: '555-8765', team: 'Tigres' },
    { player_id: 4, name: 'María Torres', CI: '44332211', faculty: 'Derecho', age: 20, email: 'maria@example.com', phone: '555-4321', team: 'Leones' },
];

export default function PlayerDetailPage({ params }: { params: { id: string } }) {
    const [player, setPlayer] = useState<Player | null>(null);
    const playerId = parseInt(params.id);

    useEffect(() => {
        const found = samplePlayers.find(p => p.player_id === playerId);
        setPlayer(found || null);
    }, [playerId]);

    if (!player) return <Container className="my-4">Player not found</Container>;

    return (
        <Container className="my-4">
            <Card>
                <Card.Header style={{ backgroundColor: 'var(--color-uh-red)', color: 'white' }}>
                    <h3>{player.name}</h3>
                </Card.Header>
                <Card.Body>
                    <p><strong>CI:</strong> {player.CI}</p>
                    <p><strong>Faculty:</strong> {player.faculty}</p>
                    <p><strong>Age:</strong> {player.age}</p>
                    <p><strong>Email:</strong> {player.email}</p>
                    <p><strong>Phone:</strong> {player.phone}</p>
                    <p><strong>Team:</strong> {player.team}</p>
                </Card.Body>
            </Card>
        </Container>
    );
}
