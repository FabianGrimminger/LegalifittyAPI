package com.example.demo;

import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import javax.persistence.*;
import java.io.Serializable;
import java.util.List;

@Entity
@EntityListeners(AuditingEntityListener.class)
public class User implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    private String name;

    @OneToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL,
            targetEntity=User.class, mappedBy = "owner")
    private List<Graffity> paintedGraffities;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<Graffity> getPaintedGraffities() {
        return paintedGraffities;
    }

    public void setPaintedGraffities(List<Graffity> paintedGraffities) {
        this.paintedGraffities = paintedGraffities;
    }
}
