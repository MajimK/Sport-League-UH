'use client';

import { useState, useEffect } from 'react';
import { Container, Table, Form, InputGroup } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

interface Player {
    player_id: number;
    name: string;
    CI: string;
    faculty: string;
}

interface PlayersTableProps {
    players: Player[];
}

export default function PlayersTableUser({ players }: PlayersTableProps) {
    const [search, setSearch] = useState('');
    const [filteredPlayers, setFilteredPlayers] = useState<Player[]>(players);
    const router = useRouter();

    useEffect(() => {
        setFilteredPlayers(
            (players || []).filter(
                p =>
                    p.name.toLowerCase().includes(search.toLowerCase()) ||
                    p.faculty.toLowerCase().includes(search.toLowerCase()) ||
                    p.CI.includes(search)
            )
        );
    }, [search, players]);

    const goToPlayer = (player_id: number) => {
        router.push(`/user/players/${player_id}`);
    };

    return (
        <Container className="my-4">
            <h2 className="mb-3" style={{ color: 'var(--color-uh-red)' }}>Players</h2>

            {/* Search */}
            <InputGroup className="mb-3">
                <InputGroup.Text style={{ backgroundColor: 'var(--color-uh-red)', color: 'white' }}>
                    <i className="bi bi-search"></i>
                </InputGroup.Text>
                <Form.Control
                    placeholder="Search by name, CI or faculty..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </InputGroup>

            {/* Table */}
            <div className="table-responsive">
                <Table striped bordered hover>
                    <thead style={{ backgroundColor: 'var(--color-uh-red)', color: 'white' }}>
                        <tr>
                            <th>ID</th>
                            <th>CI</th>
                            <th>Name</th>
                            <th>Faculty</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredPlayers.length === 0 ? (
                            <tr>
                                <td colSpan={4} className="text-center">No players found</td>
                            </tr>
                        ) : (
                            filteredPlayers.map((player) => (
                                <tr key={player.player_id} style={{ cursor: 'pointer' }} onClick={() => goToPlayer(player.player_id)}>
                                    <td>{player.player_id}</td>
                                    <td>{player.CI}</td>
                                    <td>{player.name}</td>
                                    <td>{player.faculty}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </Table>
            </div>
        </Container>
    );
}
