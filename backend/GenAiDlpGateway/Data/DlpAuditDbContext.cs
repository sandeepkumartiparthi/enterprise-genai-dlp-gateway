using GenAiDlpGateway.Models;
using Microsoft.EntityFrameworkCore;

namespace GenAiDlpGateway.Data;

public class DlpAuditDbContext : DbContext
{
    public DlpAuditDbContext(DbContextOptions<DlpAuditDbContext> options) : base(options)
    {
    }

    public DbSet<AuditLogEntry> AuditLogs => Set<AuditLogEntry>();
    public DbSet<DlpPolicyRule> PolicyRules => Set<DlpPolicyRule>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<AuditLogEntry>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.TimestampUtc);
            entity.HasIndex(e => e.ActionTaken);
            entity.HasIndex(e => e.Department);
        });

        modelBuilder.Entity<DlpPolicyRule>(entity =>
        {
            entity.HasKey(e => e.EntityType);
        });
    }
}
