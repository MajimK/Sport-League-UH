'use client';

import { useState, useEffect } from 'react';
import { Container, Table, Form, InputGroup } from 'react-bootstrap';
import { useRouter } from 'next/navigation';

interface Team {
    team_id: number;
    name: string;
    description: string;
}

interface TeamsTableProps {
    teams: Team[];
}

export default function TeamsTableUser({ teams }: TeamsTableProps) {
    const [search, setSearch] = useState('');
    const [filteredTeams, setFilteredTeams] = useState<Team[]>(teams);
    const router = useRouter();

    useEffect(() => {
        setFilteredTeams(
            (teams || []).filter(
                t =>
                    t.name.toLowerCase().includes(search.toLowerCase()) ||
                    t.description.toLowerCase().includes(search.toLowerCase())
            )
        );
    }, [search, teams]);

    const goToTeam = (team_id: number) => {
        router.push(`/user/teams/${team_id}`);
    };

    return (
        <Container className="my-4">
            <h2 className="mb-3" style={{ color: 'var(--color-uh-red)' }}>Teams</h2>

            {/* Search */}
            <InputGroup className="mb-3">
                <InputGroup.Text style={{ backgroundColor: 'var(--color-uh-red)', color: 'white' }}>
                    <i className="bi bi-search"></i>
                </InputGroup.Text>
                <Form.Control
                    placeholder="Search by name or description..."
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
                            <th>Name</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredTeams.length === 0 ? (
                            <tr>
                                <td colSpan={3} className="text-center">No teams found</td>
                            </tr>
                        ) : (
                            filteredTeams.map(team => (
                                <tr key={team.team_id} style={{ cursor: 'pointer' }} onClick={() => goToTeam(team.team_id)}>
                                    <td>{team.team_id}</td>
                                    <td>{team.name}</td>
                                    <td>{team.description}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </Table>
            </div>
        </Container>
    );
}
