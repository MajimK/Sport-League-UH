'use client';

import { useState, useEffect } from 'react';
import PlayersTableUser from '@/components/user/playersTable';
import { Container, Navbar, Nav, Form, Row, Col } from 'react-bootstrap';

interface Player {
    player_id: number;
    name: string;
    CI: string;
    faculty: string;
}

// Datos de ejemplo
const samplePlayers: Player[] = [
    { player_id: 1, name: 'Juan Pérez', CI: '12345678', faculty: 'Contabilidad' },
    { player_id: 2, name: 'Ana Gómez', CI: '87654321', faculty: 'Informática' },
    { player_id: 3, name: 'Carlos Díaz', CI: '11223344', faculty: 'Matemática' },
    { player_id: 4, name: 'María Torres', CI: '44332211', faculty: 'Derecho' },
];

export default function PlayersPage() {
    const [players, setPlayers] = useState<Player[]>(samplePlayers);
    const [search, setSearch] = useState('');
    const [token, setToken] = useState<string | null>(null);

    const fetchPlayers = async () => {
        const API_URL = process.env.NEXT_PUBLIC_API_URL;
        try {
            const storedToken = localStorage.getItem('token');
            setToken(storedToken);
            // Aquí podrías hacer tu fetch real si quieres usar API
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchPlayers();
    }, []);

    const filteredPlayers = players.filter(player =>
        player.name.toLowerCase().includes(search.toLowerCase()) ||
        player.CI.includes(search)
    );

    return (
        <>
            {/* Players Table */}
            <Container>
                <PlayersTableUser
                    players={filteredPlayers}
                />
            </Container>
        </>
    );
}
