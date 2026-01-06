'use client';

import { useState, useEffect } from 'react';
import PlayersTableUser from '@/components/user/playersTable';
import { Container, Spinner } from 'react-bootstrap';

interface Player {
    player_id: number;
    name: string;
    CI: string;
    faculty: string;
}

export default function PlayersPage() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const [players, setPlayers] = useState<Player[]>([]);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState<string | null>(null);
    const [search, setSearch] = useState('');

    const fetchPlayers = async (authToken: string | null) => {
        try {
            const headers: HeadersInit = {
                'Content-Type': 'application/json',
            };

            if (authToken) {
                headers['Authorization'] = `Bearer ${authToken}`;
            }

            const response = await fetch(`http://localhost:8000/admin/players/`, {
                headers,
                credentials: 'include',
            });

            if (!response.ok) throw new Error('Failed to fetch players');

            const playersData: Player[] = await response.json();
            setPlayers(playersData);
        } catch (err) {
            console.error('Error loading players:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const storedToken = localStorage.getItem('access_token'); // 👈 usa 'access_token' como en el primer componente
        setToken(storedToken);
        fetchPlayers(storedToken);
    }, []);

    const filteredPlayers = players.filter((player) =>
        player.name.toLowerCase().includes(search.toLowerCase()) ||
        player.CI.includes(search)
    );

    if (loading) {
        return (
            <Container className="mt-4 text-center">
                <Spinner animation="border" variant="primary" />
                <p className="mt-2">Cargando jugadores...</p>
            </Container>
        );
    }

    return (
        <Container className="mt-4">
            <h2 className="mb-4">Lista de Jugadores</h2>

            {/* Opcional: Barra de búsqueda */}
            <div className="mb-4">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Buscar por nombre o CI..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>

            <PlayersTableUser players={filteredPlayers} />
        </Container>
    );
}