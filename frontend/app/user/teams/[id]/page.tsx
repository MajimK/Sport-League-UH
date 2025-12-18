'use client';

import { useState, useEffect } from 'react';
import { Container, Card } from 'react-bootstrap';

interface Team {
    team_id: number;
    name: string;
    description: string;
    coach: string;
    members: string[];
}

// Datos de ejemplo
const sampleTeams: Team[] = [
    { team_id: 1, name: 'Los Halcones', description: 'Equipo de baloncesto masculino', coach: 'Miguel Díaz', members: ['Juan Pérez', 'Carlos Díaz'] },
    { team_id: 2, name: 'Las Águilas', description: 'Equipo de voleibol femenino', coach: 'Ana Torres', members: ['Ana Gómez', 'María Torres'] },
    { team_id: 3, name: 'Tigres', description: 'Equipo de fútbol mixto', coach: 'Luis Fernández', members: ['Carlos Díaz'] },
    { team_id: 4, name: 'Leones', description: 'Equipo de atletismo', coach: 'Rosa Martínez', members: ['María Torres'] },
];

export default function TeamDetailPage({ params }: { params: { id: string } }) {
    const [team, setTeam] = useState<Team | null>(null);
    const teamId = parseInt(params.id);

    useEffect(() => {
        const found = sampleTeams.find(t => t.team_id === teamId);
        setTeam(found || null);
    }, [teamId]);

    if (!team) return <Container className="my-4" > Team not found </Container>;

    return (
        <Container className="my-4" >
            <Card>
                <Card.Header style={{ backgroundColor: 'var(--color-uh-red)', color: 'white' }}>
                    <h3>{team.name} </h3>
                </Card.Header>
                < Card.Body >
                    <p><strong>Description: </strong> {team.description}</p >
                    <p><strong>Coach: </strong> {team.coach}</p >
                    <p><strong>Members: </strong> {team.members.join(', ')}</p >
                </Card.Body>
            </Card>
        </Container>
    );
}
